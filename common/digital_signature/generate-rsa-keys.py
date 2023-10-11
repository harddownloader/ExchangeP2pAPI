import json
import pprint
import requests
import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def create_keys():
    # generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,  # 2048 - is too small, so we use 4096
        backend=default_backend()
    )

    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(current_file_path)
        )
    )
    public_key_path = os.path.join(project_root, 'public_key.pem')
    private_key_path = os.path.join(project_root, 'private_key.pem')

    # saving the private key to a file
    with open(private_key_path, 'wb') as f:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        f.write(private_pem)

    # obtaining a public key
    public_key = private_key.public_key()

    # saving the public key to a file
    with open(public_key_path, 'wb') as f:
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        f.write(public_pem)

    return public_pem, private_pem


def main():
    create_keys()


if __name__ == "__main__":
    main()
