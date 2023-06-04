import socket

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def decrypt_file(file_path, key):
    f = Fernet(key)

    with open(file_path, "rb") as token:
        plaintext = f.decrypt(token.read())

    with open(file_path, "wb") as file:
        file.write(plaintext)


def send_encrypted_key(e_key_file_path):
    with socket.create_connection((HOST, PORT)) as sock:
        with open(e_key_file_path, "rb") as file:
            sock.send(file.read())

        decrypted_key = sock.recv(1024)

    return decrypted_key

symmetric_key = Fernet.generate_key()

FernetInstance = Fernet(symmetric_key)

HOST, PORT = "127.0.0.1", 8000

with open("../../RSA/public_key.key", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
            )

encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )

with open("encrypted_symmetric_key.key", "wb") as key_file:
    key_file.write(encrypted_symmetric_key)

decrypted_symmetric_key = send_encrypted_key("encrypted_symmetric_key.key")

file_path = "file_to_encrypt.txt"

with open(file_path, "rb") as file:
    file_data = file.read()
    encrypted_data = FernetInstance.encrypt(file_data)

with open(file_path, "wb") as file:
    file.write(encrypted_data)

decrypt_file(file_path, decrypted_symmetric_key)

quit()
