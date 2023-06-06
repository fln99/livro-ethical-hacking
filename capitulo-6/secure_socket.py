import socket
import ssl

CLIENT_KEY = "../../TLS/client.key"
CLIENT_CERT = "../../TLS/client.crt"
SERVER_CERT = "../../TLS/server.crt"

HOSTNAME = "127.0.0.1"
PORT = 8080

context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=SERVER_CERT)
context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
context.load_verify_locations(cafile=SERVER_CERT)
context.verify_mode = ssl.CERT_REQUIRED
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.PROTOCOL_TLS

with socket.create_connection((HOSTNAME, PORT)) as sock:
    with context.wrap_socket(sock, server_side=False, server_hostname=HOSTNAME) as ssock:
        print(ssock.version())
        message = input("Please enter your message: ")
        ssock.send(message.encode())
        receives = ssock.recv(1024)
        print(receives)

