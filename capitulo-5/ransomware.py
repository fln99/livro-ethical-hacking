import socket
import ssl

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
    with open(e_key_file_path, "rb") as file:
        encrypted_key = file.read()

    with socket.create_connection((HOST, PORT)) as sock:
        with setup_context().wrap_socket(sock, server_side=False, server_hostname=HOST) as ssock:
            ssock.send(encrypted_key)
            decrypted_key = ssock.recv(1024)

    return decrypted_key


def encrypt_symmetric_key():
    with open(PUBLIC_KEY, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend())

    encrypted_symmetric_key = public_key.encrypt(symmetric_key, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))
    
    return encrypted_symmetric_key


def encrypt_data(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
        encrypted_data = FernetInstance.encrypt(file_data)

    with open(file_path, "wb") as file:
        file.write(encrypted_data)


def setup_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=SERVER_CERT)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.load_verify_locations(cafile=SERVER_CERT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.options |= ssl.OP_SINGLE_ECDH_USE
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

    return context


CLIENT_KEY = "../../TLS/client.key"
CLIENT_CERT = "../../TLS/client.crt"
SERVER_CERT = "../../TLS/server.crt"

PUBLIC_KEY = "../../RSA/public_key.key"
ENCRYPTED_SK_PATH = "encrypted_symmetric_key.key"
FILE_PATH = "file_to_encrypt.txt"

HOST, PORT = "127.0.0.1", 8000

symmetric_key = Fernet.generate_key()
FernetInstance = Fernet(symmetric_key)

encrypted_symmetric_key = encrypt_symmetric_key()

with open(ENCRYPTED_SK_PATH, "wb") as key_file:
    key_file.write(encrypted_symmetric_key)

encrypt_data(FILE_PATH)

decrypted_symmetric_key = send_encrypted_key(ENCRYPTED_SK_PATH)

decrypt_file(FILE_PATH, decrypted_symmetric_key)

quit()