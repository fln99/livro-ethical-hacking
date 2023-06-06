import socket
import ssl

CLIENT_CERT = "../../TLS/client.crt"
SERVER_KEY = "../../TLS/server.key"
SERVER_CERT = "../../TLS/server.crt"

PORT = 8080

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile=CLIENT_CERT)
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.PROTOCOL_TLS

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(("", PORT))
    sock.listen(1)

    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print(addr)
        message = conn.recv(1024).decode()
        capitalizedMessage = message.upper()
        conn.send(capitalizedMessage.encode())
