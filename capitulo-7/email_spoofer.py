import sys, socket

SIZE = 1024

def send_message(smtp_server, port, from_address, to_address, message):
    IP = smtp_server
    PORT = int(port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    
    print(s.recv(SIZE).decode())

    s.send(b"HELO " + from_address.split("@")[1].encode() + b"\n")
    print(s.recv(SIZE).decode())

    s.send(b"MAIL FROM:<" + from_address.encode() + b">\n")
    print(s.recv(SIZE).decode())

    s.send(b"RCPT TO:<" + to_address.encode() + b">\n")
    print(s.recv(SIZE).decode())

    s.send(b"DATA\n")
    print(s.recv(SIZE).decode())

    s.send(message.encode() + b"\n")
    s.send(b"\r\n.\r\n")
    print(s.recv(SIZE).decode())

    s.send(b"QUIT\n")
    print(s.recv(SIZE).decode())
    s.close()


def main(args):
    smtp_server = args[1]
    port = args[2]
    from_address = args[3]
    to_address = args[4]
    message = args[5]

    send_message(smtp_server, port, from_address, to_address, message)


if __name__ == "__main__":
    main(sys.argv)