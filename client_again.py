from socket import *
import threading
import concurrent.futures
import time

server_host = 'localhost'
server_port = 3291
client_port = 3478
instrux = "Type a message. " \
          "Type /f when you are finished sending messages are ready to wait for a response."
quit_msg = "Type /q to quit"


# def server_thread_func(sckt, event):
def get_messages(sckt):
    # while not event.is_set():
    server_msg = sckt.recv(1024).decode()
    while server_msg[-2:] != '/f':
        print(f"SERVER: {server_msg}")
        server_msg = sckt.recv(1024).decode()
        if server_msg[-2:] == '/f':
            print(f"SERVER: {server_msg[:-2]}")
        # time.sleep(2)

    # event.set()


# def client_thread_func(sckt, event):
def send_message(sckt):
    print(f"Type a message")
    #while not event.is_set():
    # client_msg = input('> ')
    # while client_msg[-2:] != '/f':
    while True:
        client_msg = input('> ')
        if client_msg == "/q":
            print(f"Closing connection")
            sckt.close()
            # client_sock.close()
            # event.set()
            return
        # else:
        # sckt.send(str(client_msg_len))
        sckt.send(client_msg.encode())
        if client_msg[-2:] == '/f':
            break


with socket(AF_INET, SOCK_STREAM) as client_sock:
    client_sock.connect((server_host, server_port))
    print(instrux)
    print(quit_msg)
    while True:
        send_message(client_sock)
        get_messages(client_sock)
    # while client_msg != '/q':
    # event = threading.Event()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.submit(client_thread_func, client_sock, event)
    #     executor.submit(server_thread_func, client_sock, event)
    #     executor.shutdown(wait=False, cancel_futures=True)
        # client_sock.close()
