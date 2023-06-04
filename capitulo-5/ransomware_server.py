import socketserver

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class ClientHandler(socketserver.BaseRequestHandler):

    def handle(self):
        encrypted_key = self.request.recv(1024).strip()
        
        with open("../../RSA/pub_priv_pair.key", "rb") as pkey_file:
            private_key = serialization.load_pem_private_key(
                    pkey_file.read(),
                    password=None,
                    )
        
        plaintext = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                    )
                )
        
        self.request.sendall(plaintext)


if __name__ == "__main__":
    HOST, PORT = "", 8000

    tcp_server = socketserver.TCPServer((HOST, PORT), ClientHandler)

    try:
        print("[+] Starting server...")
        tcp_server.serve_forever()
    except:
        print("[!] Something went wrong.")
