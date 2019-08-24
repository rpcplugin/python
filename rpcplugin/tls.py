import base64
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import six


def generate_certificate():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, six.text_type("localhost"))
    ])
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1000)
        .not_valid_before(now - datetime.timedelta(seconds=30))
        .not_valid_after(now + datetime.timedelta(hours=262980))
        .add_extension(basic_contraints, False)
        .sign(key, hashes.SHA256(), default_backend())
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return [key_pem, cert_pem]


def raw_base64_to_pem_cert(s):
    # We'll first round-trip through the base64 library to normalize any
    # required padding, which not all server implementations include when
    # generating their raw base64 certs.
    s = base64.standard_b64encode(base64.standard_b64decode(s+'==='))

    l = 64
    lines = (s[i:i+l] for i in range(0, len(s), l))
    return (
        '-----BEGIN CERTIFICATE-----\n' +
        "\n".join(lines) +
        '\n-----END CERTIFICATE-----\n'
    )
