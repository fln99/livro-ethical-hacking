import socketserver

class ClientHandler(socketserver.BaseRequestHandler):

    def handle(self):
        encrypted_key = self.request.recv(1024).strip()
        
        # TODO: key decryption
        
        # once decrypted, send via self.request.sendall("key")

if __name__ == "__main__":
    HOST, PORT = "", 8000

    tcp_server = socketserver.TCPServer((HOST, PORT), ClientHandler)

    try:
        print("[+] Starting server...")
        tcp_server.serve_forever()
    except:
        print("[!] Something went wrong.")
