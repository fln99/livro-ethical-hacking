import socket
import ssl

client_cert = "../../TLS/client.crt"
server_key = "../../TLS/server.key"
server_cert = "../../TLS/server.crt"
port = 8080

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile=client_cert)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.PROTOCOL_TLS

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(("", port))
    sock.listen(1)

    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print(addr)
        message = conn.recv(1024).decode()
        capitalizedMessage = message.upper()
        conn.send(capitalizedMessage.encode())
