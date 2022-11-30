# CITATION:
# Python docs. How to: Socket programming

# CITATION:
# My Python socket project from the beginning of this term
#
# Use of two ports, one for send one for receive, from instructor's
# reply in Ed discussion board:
# https://edstem.org/us/courses/29340/discussion/2175842
from socket import *
import threading
import logging
import time
import concurrent.futures

server_host = "localhost"
server_send_port = 3291
server_receive_port = 8000
initial_msg = "Waiting for messages..."
quit_msg = "Type /q to quit."
msg_num = 0


def client_thread_func(conn, event):
    while not event.is_set():
        # Receive data from the client, with bufsize specified
        client_data = conn.recv(1024).decode()
        while len(client_data) > 0:
            print(client_data)
            client_data = conn.recv(1024).decode()

        event.set()

        # data_remaining = client_data.split(' ')[0]
        # print(client_data[len(data_remaining)+1:])
        # data_remaining -= len(client_data[len(data_remaining)+1:])
        # while data_remaining > 0:
        #     client_data = conn.recv(1024).decode()
        #     print(client_data)
        #     data_remaining -= len(client_data)

        # print(f"CLIENT DATA: {client_data}")
        # if len(client_data) > 0:
        #     print(f"CLIENT MESSAGE LENGTH: {len(client_data)}")
        #     msg_num += 1
        #     if msg_num == 1:
        #         print(quit_msg)
        #     print(client_data.decode())
        # else:
        #     break

        # print("No client data")


def server_thread_func(conn, event):
    while not event.is_set():
        server_reply = input('> ')
        server_reply = server_reply + '\n'
        if server_reply == '/q':
            print(f"Closing connection")
            event.set()
            conn.close()
            return
        conn.send(server_reply.encode())


with socket(AF_INET, SOCK_STREAM) as sock:
    # Use of setsockopt taken from the project instructions
    # to help avoid "hanging" a port during testing
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((server_host, server_send_port))
    sock.listen(1)  # Does not connect to multiple clients
    print(f"Server listening on: {server_host} on port: {server_receive_port}")
    conn, addr = sock.accept()
    with conn:
        print(f"Connected by ({addr})\n"
              f"{initial_msg}")
        event = threading.Event()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(client_thread_func, conn, event)
            executor.submit(server_thread_func, conn, event)

