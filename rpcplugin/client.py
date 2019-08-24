import copy
import datetime
import os
import subprocess

import grpc

import rpcplugin.tls


def start(
    args,
    handshake,
    proto_versions,
    tls_credentials=None,
    stderr=None,
):
    if handshake is None or handshake.cookie_key is None or handshake.cookie_value is None:
        raise ValueError(
            "handshake must be set and must have cookie key and value",
        )

    if proto_versions is None or len(proto_versions) == 0:
        raise ValueError(
            "proto_versions must be a map with at least one protocol version defined"
        )

    if args is None or len(args) == 0:
        raise ValueError(
            "args must be a sequence with at least one element giving the plugin program to run"
        )

    version_strings = ','.join((str(v) for v in proto_versions.keys()))
    environ = copy.copy(os.environ)
    environ[handshake.cookie_key] = handshake.cookie_value
    environ["PLUGIN_PROTOCOL_VERSIONS"] = version_strings
    environ["PLUGIN_TRANSPORTS"] = "unix,tcp"

    auto_tls_cert = None
    if tls_credentials is None:
        auto_tls_cert = rpcplugin.tls.generate_certificate()
        # The certificate in PEM format
        environ['PLUGIN_CLIENT_CERT'] = auto_tls_cert[1]

    proc = subprocess.Popen(
        args,
        env=environ,
        stdout=subprocess.PIPE,  # so we can read the handshake
        stderr=stderr,
    )

    raw = proc.stdout.readline().strip()
    parts = raw.split("|", 6)
    if len(parts) < 5:
        raise HandshakeError(
            'invalid handshake message from the plugin server',
        )
    if parts[0] != '1':
        raise HandshakeError(
            'invalid handshake version %s from the plugin server' % parts[0],
        )
    if parts[4] != 'grpc':
        raise HandshakeError(
            'invalid RPC protocol %s from the plugin server' % parts[4],
        )

    try:
        proto_version = int(parts[1])
    except:
        raise HandshakeError(
            'invalid plugin protocol version %s from the plugin server' % parts[1],
        )

    if proto_version not in proto_versions:
        raise HandshakeError(
            'plugin server selected unsupported protocol version %i' % proto_version,
        )

    client_builder = proto_versions[proto_version]

    if len(parts) >= 6 and len(parts[5]) > 50 and auto_tls_cert is not None:
        # This is the server's auto-negotiated TLS certificate, given as
        # a direct base64 encoding of its DER bytes. The GRPC library wants
        # it PEM-encoded, so we'll add PEM header and footer to it.
        server_cert_pem = rpcplugin.tls.raw_base64_to_pem_cert(parts[5])
        tls_credentials = grpc.ssl_channel_credentials(
            root_certificates=server_cert_pem,
            private_key=auto_tls_cert[0],
            certificate_chain=auto_tls_cert[1],
        )
    elif tls_credentials is None:
        raise HandshakeError(
            'plugin server did not return a TLS certificate in auto-TLS mode',
        )

    if parts[2] == 'tcp':
        host, port = parts[3].split(':')
        port = int(port)
        if host == '127.0.0.1':
            host = 'localhost'  # so that a localhost certificate will work
        addr = '%s:%d' % (host, port)
    elif parts[2] == 'unix':
        addr = "unix:" + parts[3]
        chan = grpc.secure_channel(
            addr,
            tls_credentials,
        )
    else:
        raise HandshakeError(
            'plugin server selected unsupported transport protocol %s' % parts[2],
        )

    return Plugin(
        proto_version=proto_version,
        client_builder=client_builder,
        proc=proc,
        addr=addr,
        tls_credentials=tls_credentials,
    )


class Plugin(object):
    def __init__(self, proto_version, client_builder, proc, addr, tls_credentials):
        self.proto_version = proto_version
        self.client_builder = client_builder
        self.proc = proc
        self.addr = addr
        self.tls_credentials = tls_credentials

    def client(self):
        chan = grpc.secure_channel(
            self.addr,
            self.tls_credentials,
        )
        client = self.client_builder(chan)
        return (self.proto_version, client)

    def close(self):
        self.proc.terminate()

        # Consume any stdout leftovers and wait for the process to terminate
        self.proc.communicate()


class HandshakeError(Exception):
    pass


__all__ = [
    'HandshakeError',
    'Plugin',
    'start',
]
