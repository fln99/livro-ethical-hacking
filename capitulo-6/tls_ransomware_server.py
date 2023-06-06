import socket
import ssl
import threading

client_cert = "../../TLS/client.crt"
server_key = "../../TLS/server.key"
server_cert = "../../TLS/server.crt"

port = 8080

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile=client_cert)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

def handler(conn):
    encrypted_key = conn.recv(4096).decode()

    # decryption code here

    conn.send(decrypted_key.encode())
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(("", port))
    sock.listen(5)

    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            print(addr)
            handler_thread = threading.Thread(target=handler, args=(conn,))
            handler_thread.start()
