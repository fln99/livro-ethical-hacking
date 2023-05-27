import socket
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

client, address = server.accept()

client.send(b"[+] Welcome to the server.\n")

while True:
    message = client.recv(1024).decode()

    if message.strip() == "bye" or not message:
        break

    client.send(message.encode())

server.close()
