# CITATION:
# Python docs. How to: Socket programming

# CITATION:
# My Python socket project from the beginning of this term
from socket import *

server_host = "localhost"
server_port = 3291
initial_msg = "Waiting for messages..."
quit_msg = "Type /q to quit."
msg_num = 0

with socket(AF_INET, SOCK_STREAM) as sock:
    # Use of setsockopt taken from the project instructions
    # to help avoid "hanging" a port during testing
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((server_host, server_port))
    sock.listen(1)  # Does not connect to multiple clients
    conn, addr = sock.accept()
    with conn:
        print(f"Connected by ({conn}, {addr})\n"
              f"{initial_msg}")
        while True:
            # Receive data from the client, with bufsize specified
            client_data = conn.recv(1024)
            if len(client_data) > 0:
                msg_num += 1
                if msg_num == 1:
                    print(quit_msg)
                print(client_data)
            else:
                break

        server_reply = input('> ')
        if server_reply == "/q":
            sock.close()
        conn.send(server_reply.encode())


if __name__ == '__main__':
    print(f"Server listening on: {server_host} on port: {server_port}")
