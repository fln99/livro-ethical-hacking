import socket
import ssl
import threading

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

CLIENT_CERT = "../../TLS/client.crt"
SERVER_KEY = "../../TLS/server.key"
SERVER_CERT = "../../TLS/server.crt"
PRIVATE_KEY = "../../RSA/pub_priv_pair.key"

PORT = 8000

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile=CLIENT_CERT)
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

def handler(conn):
    encrypted_key = conn.recv(1024).strip()

    with open(PRIVATE_KEY, "rb") as pkey_file:
            private_key = serialization.load_pem_private_key(pkey_file.read(), password=None)
        
    decrypted_key = private_key.decrypt(encrypted_key, padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None))

    conn.send(decrypted_key)
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(("", PORT))
    sock.listen(5)

    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            print(addr)
            handler_thread = threading.Thread(target=handler, args=(conn,))
            handler_thread.start()
