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
        key_size=2048,
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
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    public_key_path = os.path.join(project_root, 'public_key.pem')
    private_key_path = os.path.join(project_root, 'private_key.pem')

    with open(public_key_path, 'rb') as key_file:
        public_key_pem = key_file.read()

    with open(private_key_path, 'rb') as key_file:
        private_key_pem = key_file.read()

    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())

    # ==================================================
    data_to_send = {
        "field1": "value1",
        "field2": "value2",
        # other data
    }

    api_url = "http://localhost:7000/api/v1/callback/1/"

    your_access_token = 'some token'
    # set headers for request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {your_access_token}",  # Если требуется аутентификация на другом API
    }


    data_bytes = json.dumps(data_to_send).encode('utf-8')
    encrypted_data = public_key.encrypt(
        data_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    pprint.pprint({
        'encrypted_data': encrypted_data
    })

    received_encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    # pprint.pprint(received_encrypted_data_base64)

    body = {
        'data': received_encrypted_data_base64
    }

    # WE CAN CHECK DECRYPTION HERE
    # received_encrypted_data = base64.b64decode(received_encrypted_data_base64)
    # decrypted_data = private_key.decrypt(
    #     received_encrypted_data,
    #     padding.OAEP(
    #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #         algorithm=hashes.SHA256(),
    #         label=None
    #     )
    # )
    # pprint.pprint('decrypted_data:')
    # pprint.pprint(decrypted_data)
    # received_data = json.loads(decrypted_data.decode('utf-8'))
    # print('received_data data:')
    # pprint.pprint(received_data)

    # send patch request
    try:
        response = requests.patch(api_url, json=body, headers=headers)
        response.raise_for_status()  # check has it success status

        # giving response
        response_data = response.json()
        print("Response from another API:", response_data)
    except requests.exceptions.RequestException as e:
        # catch errors
        print("The request was failed, error:", e)


if __name__ == "__main__":
    # create_keys()
    main()
