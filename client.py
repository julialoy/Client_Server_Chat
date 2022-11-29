from socket import *

server_host = 'localhost'
server_port = 3291
client_port = 3478
quit_msg = "Type /q to quit"

with socket(AF_INET, SOCK_STREAM) as client_sock:
    client_sock.connect((server_host, server_port))
    while True:
        client_msg = input('> ')

        if client_msg == "/q":
            client_sock.close()
        else:
            client_sock.send(client_msg.encode())
            server_msg = client_sock.recv(1024)
            while len(server_msg) > 0:
                print(server_msg)
                client_sock.recv(1024)
                