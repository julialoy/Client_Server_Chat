from socket import *


# CITATION:
# Use of class for client was inspired by and adapted from the MySocket
# example at
# https://docs.python.org/3.4/howto/sockets.html
class Client:
    """Server object creates a server and tracks the server state."""
    def __init__(self):
        self._host = 'localhost'
        self._port = 3291
        # self._client_port = 3478
        self._instrux = "Type a message.\nType /f when you are finished sending messages are ready to wait for a response."
        self._quit_msg = "Type /q to quit"
        self._is_connected = False
        self._hangman_started = False

    def _get_messages(self, sckt):
        if not self._is_connected:
            return

        server_msg = sckt.recv(1024).decode()
        while server_msg[-2:] != '/f':
            if not self._hangman_started:
                print(f"SERVER: {server_msg}")
            elif len(server_msg) > 0:
                print(server_msg)

            server_msg = sckt.recv(1024).decode()
            if server_msg[-2:] == '/f' and len(server_msg) > 2:
                print(f"SERVER: {server_msg[:-2]}")
            elif server_msg == '/hangman':
                self._hangman_started = True


    def _send_message(self, sckt):
        if not self._is_connected:
            return

        client_msg = input('> ')
        sckt.send(client_msg.encode())

        while not self._hangman_started:
            client_msg = input('> ')
            sckt.send(client_msg.encode())
            if client_msg == "/q":
                print(f"Closing connection")
                self._is_connected = False
                break
            if client_msg[-2:] == '/f':
                break

    def client_run(self):
        with socket(AF_INET, SOCK_STREAM) as client_sock:
            client_sock.connect((self._host, self._port))
            self._is_connected = True
            print(self._instrux)
            print(self._quit_msg)
            while self._is_connected:
                self._send_message(client_sock)
                self._get_messages(client_sock)


if __name__ == '__main__':
    new_client = Client()
    new_client.client_run()
