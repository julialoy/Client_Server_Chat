# CITATION:
# Python docs. How to: Socket programming

# CITATION:
# My Python socket project from the beginning of this term
#
# Use of two ports, one for send one for receive, from instructor's
# reply in Ed discussion board:
# https://edstem.org/us/courses/29340/discussion/2175842
from socket import *

server_host = "localhost"
server_send_port = 3291
server_receive_port = 8000
initial_msg = "Waiting for messages..."
instrux = "Enter a message..."
instrux2 = "Type /f when finished writing.\n" \
           "Type /q to quit."
is_first_reply = True
hangman_started = False


def get_client_data(conn):
    client_data = conn.recv(1024).decode()
    while client_data[-2:] != '/f':
        print(f"CLIENT: {client_data}")
        # print(f"(Last 3 chars = {client_data[-4:-1]}")
        # prev_char = client_data
        client_data = conn.recv(1024).decode()
        if client_data[-2:] == '/f':
            print(f"CLIENT: {client_data[:-2]}")


def send_data(conn):
    if is_first_reply:
        print(instrux)
        print(instrux2)
        # is_first_reply = False
    # server_reply = input('> ')
    # while server_reply[-2:] != '/f':
    while True:
        server_reply = input('> ')
        # server_reply = server_reply
        if server_reply == '/q':
            print(f"Closing connection")
            # return True
            conn.close()
            return
        conn.send(server_reply.encode())
        if server_reply[-2:] == '/f':
            break


with socket(AF_INET, SOCK_STREAM) as sock:
    # Use of setsockopt taken from the project instructions
    # to help avoid "hanging" a port during testing
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((server_host, server_send_port))
    sock.listen(1)  # Does not connect to multiple clients
    print(f"Server listening on: {server_host} on port: {server_receive_port}")
    conn, addr = sock.accept()
    # sock.setblocking(False) # We don't want the recv to block the rest of the server's functionality
    with conn:
        print(f"Connected by ({addr})\n"
              f"{initial_msg}")
        # Receive data from the client, with bufsize specified
        # get_client_data(conn)
        while True:
            # print(f"READ: {read_sockets}, WRITE: {write_socks}, ERROR: {error_sockets}")
            get_client_data(conn)

            send_data(conn)
            if is_first_reply:
                is_first_reply = False
                # should_continue = send_data(conn)
                # client_data = input('> ')
                # input_timer.cancel()
                # continue


        # conn.close()


