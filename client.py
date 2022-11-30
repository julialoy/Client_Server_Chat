from socket import *
import threading
import concurrent.futures

server_host = 'localhost'
server_port = 3291
client_port = 3478
quit_msg = "Type /q to quit"

def server_thread_func(sckt, event):
    while not event.is_set():
        server_msg = sckt.recv(1024)
        while len(server_msg) > 0:
            print(f"SERVER MESSAGE LENGTH: {len(server_msg)}")
            print(server_msg.decode())
            server_msg = sckt.recv(1024)

        event.set()

def client_thread_func(sckt, event):
    print(f"Type a message")
    while not event.is_set():
        client_msg = input('> ')
        client_msg_len = len(client_msg)
        if client_msg == "/q":
            print(f"Closing connection")
            # client_sock.close()
            event.set()
            return
        # else:
        client_data = str(client_msg_len) + ' ' + client_msg
        sckt.send(client_data.encode())


with socket(AF_INET, SOCK_STREAM) as client_sock:
    client_sock.connect((server_host, server_port))
    print(quit_msg)
    # while client_msg != '/q':
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(client_thread_func, client_sock, event)
        executor.submit(server_thread_func, client_sock, event)

