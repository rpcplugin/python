from concurrent import futures
import os
import signal
import time

import grpc
from grpc_health.v1.health import HealthServicer
from grpc_health.v1 import health_pb2, health_pb2_grpc

import rpcplugin.tls


def serve(
    handshake,
    proto_versions,
    tls_credentials=None,
    signal_handlers=True,
):
    """
    Start up a plugin server for the given protocol versions and announce it
    on stdout using the rpcplugin handshake.

    This function blocks until the client asks the server to exit.
    """

    if handshake == None or handshake.cookie_key == None or handshake.cookie_value == None:
        raise ValueError(
            "handshake must be set and must have cookie key and value",
        )

    if proto_versions == None or len(proto_versions) == 0:
        raise ValueError(
            "proto_versions must be a map with at least one protocol version defined"
        )

    got_cookie_value = os.environ.get(handshake.cookie_key, "")
    if got_cookie_value != handshake.cookie_value:
        raise Exception(
            "calling program is not an rpcplugin host",
        )

    try:
        (v, impl) = _negotiate_protocol_version(proto_versions)
    except TypeError:
        raise Exception(
            "cannot support any protocol versions offered by the plugin client"
        )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Plugin healthcheck service is mandatory for rpcplugin servers
    health = HealthServicer()
    health.set(
        "plugin",
        health_pb2.HealthCheckResponse.ServingStatus.Value('SERVING'),
    )

    health_pb2_grpc.add_HealthServicer_to_server(health, server)
    impl(server)

    auto_cert_str = ""
    if tls_credentials == None:
        (creds, cert_str) = _auto_tls()
        tls_credentials = creds
        auto_cert_str = cert_str

    port = server.add_secure_port('0.0.0.0:0', tls_credentials)

    if signal_handlers:
        # Ignore interrupt signals, because they're probably being sent to
        # the whole process group and we want the host program to handle
        # them, and decide for itself when it's time for this plugin server
        # to exit.
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    server.start()

    # This handshake line tells the client where to connect and what protocol
    # to talk when it does.
    print("1|%d|tcp|127.0.0.1:%d|grpc|%s" % (v, port, str(auto_cert_str)))

    while True:
        time.sleep(60 * 60 * 24)


def _negotiate_protocol_version(supported_versions):
    possible_versions_str = os.environ.get("PLUGIN_PROTOCOL_VERSIONS", "")
    if possible_versions_str == "":
        # Client isn't performing the negotiation protocol properly, so
        # negotiation fails.
        return None

    possible_versions = reversed(sorted(
        [int(v) for v in possible_versions_str.split(",")],
    ))

    for v in possible_versions:
        if v in supported_versions:
            return (v, supported_versions[v])

    return None


def _auto_tls():
    client_cert = os.environ["PLUGIN_CLIENT_CERT"]
    server_cert = rpcplugin.tls.generate_certificate()

    # HACK: The rpcplugin protocol wants just a straight base64 encoding of
    # the server certificate, but the cryptography library doesn't have a
    # facility to produce that directly, so we'll extract the base64
    # characters out of the PEM encoding instead.
    cert_pem_lines = server_cert[1].decode('us-ascii').split('\n')
    cert_pem_lines = cert_pem_lines[1:-2]
    cert_b64 = ''.join(cert_pem_lines)

    return (grpc.ssl_server_credentials(
        [server_cert],
        client_cert,
        require_client_auth=True,
    ), cert_b64)


__all__ = [
    'serve',
]
