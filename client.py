from socket import *

from hangman import HangmanGame


# CITATION:
# Use of class for client was inspired by and adapted from
# McMillan, G. (Nov. 30, 2022). MySocket code example in "Socket Programming
# HOWTO" in Python documentation. [Python docs v. 3.4.10]
# https://docs.python.org/3.4/howto/sockets.html
class Client:
    """Client object creates a client chat and tracks the various states, including
    connection, and whether the Server and Client have started a game of
    Hangman.
    """
    def __init__(self):
        self._host = 'localhost'
        self._port = 3291
        self._instrux = ("Type a message.\n"
                         "  * Type /f after sending the messages you wish to send.\n"
                         "  * Type /hangman to start a Hangman game.\n"
                         "  * Type /q to quit.")
        self._is_connected = False
        self._hangman_started = False
        self._socket = None
        self._is_recv_msgs = False

    def _get_messages(self):
        """Handles retrieving any messages from the server."""
        if not self._is_connected:
            return

        self._is_recv_msgs = True

        # CITATION:
        # Use of delimiter to indicate when server has finished sending
        # messages is based on information in
        # McMillan, G. (Nov. 30, 2022). "Socket Programming
        # HOWTO" in Python documentation. [Python docs v. 3.4.10]
        # https://docs.python.org/3.4/howto/sockets.html
        while self._is_recv_msgs:
            server_msg = self._socket.recv(1024).decode()
            if '/hangman' in server_msg:
                self._hangman_started = True

            if '/f' in server_msg and len(server_msg) > 2 and not self._hangman_started:
                server_msg = server_msg.replace('/f', '')
                print(f"SERVER: {server_msg}")
                self._is_recv_msgs = False
            elif '/f' in server_msg and len(server_msg) > 2:
                if '/endhangman' in server_msg:
                    self._hangman_started = False
                    # Remove the end command
                    # Use of Python's replace method to easily remove
                    # the substring and leave /f in place
                    server_msg = server_msg.replace('/endhangman', '')
                server_msg = server_msg.replace('/f', '')
                print(server_msg)
                self._is_recv_msgs = False
            elif '/f' in server_msg:
                self._is_recv_msgs = False
            elif '/q' in server_msg:
                self._is_connected = False
                print("Server closed connection.")
                self._is_recv_msgs = False
            elif len(server_msg) > 0 and not self._hangman_started:
                print(f"SERVER: {server_msg}")
            elif len(server_msg) > 0 and server_msg != '/hangman':
                if '/endhangman' in server_msg:
                    self._hangman_started = False
                    server_msg = server_msg.replace('/endhangman', '')
                print(server_msg)

    def _send_message(self):
        """Handles sending messages to the server."""
        if not self._is_connected:
            return

        # Hangman game is turn based, client will only enter one input
        if self._hangman_started:
            client_msg = input('> ')
            self._socket.sendall(client_msg.encode())

        # When not playing Hangman, client can send as many messages as
        # desired
        while not self._hangman_started:
            client_msg = input('> ')
            self._socket.sendall(client_msg.encode())
            if client_msg == "/q":
                print(f"Closing connection")
                self._is_connected = False
                break
            elif client_msg[-2:] == '/f':
                break
            elif client_msg == '/hangman':
                self._hangman_started = True
                self.play_hangman()
                break

    def play_hangman(self):
        new_game = HangmanGame(self._socket, "CLIENT", "SERVER")
        new_game.play_hangman()
        self._hangman_started = False

    def client_run(self):
        # CITATION:
        # Creation of the socket adapted from my Sockets and HTTP programming
        # project for this course this term:
        # Loy, J. Sockets and HTTP programming project for OSU CS372, Fall
        # 2022. [Source code.]
        #
        # The original citations from my Sockets and HTTP project are still
        # relevant and are listed below:
        #
        # This code has been adapted from the Python socket documentation,
        # specifically the client socket example in the documentation, and from
        # the example from the course textbook:
        #
        # Kurose, J., and Ross, K. Chapter 2, Section 2.7.2, "Socket
        # Programming with TCP," in Computer Networking, 8e. [Code examples].
        # Hoboken, NJ: Pearson, 2021.
        #
        # Python documentation. (Oct. 13, 2022) "Socket - Low-Level
        # Networking Interface." (Python v. 3.10.8).
        # https://docs.python.org/3/library/socket.html
        with socket(AF_INET, SOCK_STREAM) as client_sock:
            client_sock.connect((self._host, self._port))
            self._is_connected = True
            self._socket = client_sock
            print(self._instrux)
            while self._is_connected:
                self._send_message()

                # Client shuts down if server leaves connection
                if not self._is_connected:
                    client_sock.close()

                self._get_messages()


if __name__ == '__main__':
    new_client = Client()
    new_client.client_run()
