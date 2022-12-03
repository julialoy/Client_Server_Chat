from socket import *

from hangman import HangmanGame


# CITATION:
# Use of class for server was inspired by and adapted from
# McMillan, G. (Nov. 30, 2022). MySocket code example in "Socket Programming
# HOWTO" in Python documentation. [Python docs v. 3.4.10]
# https://docs.python.org/3.4/howto/sockets.html
class Server:
    """Server object creates a server chat and tracks the various states, including
    connection, whether a message has been received from a client, and
    whether the Server and Client are playing a game of Hangman.
    """
    def __init__(self):
        self._host = 'localhost'
        self._port = 3291
        self._initial_msg = "Waiting for messages..."
        self._instrux = ("Type a message.\n"
                         "  * Type /f after sending the messages you wish to send.\n"
                         "  * Type /hangman to start a Hangman game.\n"
                         "  * Type /q to quit.")
        self._is_first_reply = True
        self._hangman_started = False
        self._is_connected = False
        self._hangman_game = None

    def _get_client_data(self, conn):
        """Handles retrieving any messages from the client."""
        if not self._is_connected:
            return
        # client_data = conn.recv(1024).decode()
        # CITATION:
        # Use of delimiter to indicate when client has finished sending
        # messages is based on information in
        # McMillan, G. (Nov. 30, 2022). "Socket Programming
        # HOWTO" in Python documentation. [Python docs v. 3.4.10]
        # https://docs.python.org/3.4/howto/sockets.html
        # while client_data[-2:] != '/f':
        while True:
            client_data = conn.recv(1024).decode()
            if '/hangman' in client_data:
                self._hangman_started = True

            if client_data[-2:] == '/f' and len(client_data) > 2 and not self._hangman_started:
                print(f"CLIENT: {client_data[:-2]}")
                break
            elif client_data[-2:] == '/f' and len(client_data):
                print(client_data[:-2])
                if '/endhangman' in client_data:
                    self._hangman_started = False
                break
            elif client_data[-2:] == '/q':
                self._is_connected = False
                print("Client left the connection. Closing connection.")
                break
            elif len(client_data) > 0 and not self._hangman_started:
                print(f"CLIENT: {client_data}")
            elif len(client_data) > 0 and client_data != '/hangman':
                if '/endhangman' in client_data:
                    self._hangman_started = False
                print(client_data)

    def _send_data(self, conn):
        """Handles sending messages to the client."""
        if not self._is_connected:
            return

        # Hangman game is turn based, server will only enter one input
        if self._hangman_started:
            server_reply = input('> ')
            conn.sendall(server_reply.encode())

        # When not playing Hangman, server can send as many messages
        # as desired
        while not self._hangman_started:
             # print(f"NO HANGMAN GAME. SEND A MESSAGE.")
            server_reply = input('> ')
            conn.sendall(server_reply.encode())
            if server_reply == '/q':
                print(f"Closing connection")
                self._is_connected = False
                break
            elif server_reply[-2:] == '/f':
                break
            elif server_reply == '/hangman':
                self._hangman_started = True
                # self.play_hangman(conn)
                self.play_hangman(conn)
                break

    def play_hangman(self, conn):
        new_game = HangmanGame(conn, "SERVER", "CLIENT")
        new_game.play_hangman()
        self._hangman_game = None
        self._hangman_started = False
    #
    # def send_client_hangman(self, conn, data):
    #     data = data
    #     conn.send(data.encode())
    #
    # def recv_client_hangman(self, conn):
    #     client_guess = conn.recv(1).decode()
    #     return client_guess
    #
    # def play_hangman(self, conn, player_number=1):
    #     if player_number == 1:
    #         new_game = HangmanGame()
    #         self._hangman_game = new_game
    #
    #     print(self._hangman_game.instructions)
    #     self.send_client_hangman(conn, self._hangman_game.instructions)
    #     while not self._hangman_game.get_game_over():
    #         game_progress = self._hangman_game.get_game_progress()
    #         print(game_progress)
    #         self.send_client_hangman(conn, game_progress)
    #
    #         guessed_letters = self._hangman_game.get_letters_guessed()
    #         if guessed_letters:
    #             print(guessed_letters)
    #             self.send_client_hangman(conn, guessed_letters)
    #
    #         if self._hangman_game.get_player_turn() == 1:
    #             self.send_client_hangman(conn, "SERVER IS GUESSING")
    #             server_guess = self._hangman_game.get_player_guess()
    #             self.send_client_hangman(conn, f"SERVER GUESSED {server_guess}")
    #             game_response = self._hangman_game.get_guess_result(server_guess)
    #             print(game_response)
    #             self.send_client_hangman(conn, game_response+'\n')
    #         else:
    #             print("CLIENT IS GUESSING")
    #             self.send_client_hangman(conn, "Guess a letter: ")
    #             self.send_client_hangman(conn, '/f')
    #             client_guess = self.recv_client_hangman(conn)
    #             print(f"CLIENT GUESSED {client_guess}")
    #             game_response = self._hangman_game.get_guess_result(client_guess)
    #             print(game_response)
    #             self.send_client_hangman(conn, game_response+'\n')
    #
    #         self._hangman_game.advance_turn()
    #
    #     self._hangman_game = None
    #     self._hangman_started = False
    #     "******************* GAME OVER *******************************"
    #     self.send_client_hangman(conn, '/endhangman')
    #     self.send_client_hangman(conn, '/f')

    def server_run(self):
        # CITATION:
        # Creation of the socket adapted from my Sockets and HTTP programming
        # project for this course this term:
        # Loy, J. Sockets and HTTP programming project for OSU CS372, Fall
        # 2022. [Source code.]
        #
        # The original citations from my Sockets and HTTP project are still
        # relevant and are listed below:
        #
        # This code has also been adapted from the Python socket documentation,
        # specifically the server socket example in the documentation, and from
        # the example from the course textbook:
        #
        # Kurose, J., and Ross, K. Chapter 2, Section 2.7.2, "Socket
        # Programming with TCP," in Computer Networking, 8e. [Code examples]
        # Hoboken, NJ: Pearson, 2021.
        #
        # Python documentation. (Oct. 13, 2022) "Socket - Low-Level
        # Networking Interface." (Python v. 3.10.8).
        # https://docs.python.org/3/library/socket.html
        with socket(AF_INET, SOCK_STREAM) as sock:
            # Use of setsockopt taken from the project instructions
            # to help avoid "hanging" a port during testing
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((self._host, self._port))
            sock.listen(1)  # Does not handle multiple connections
            print(f"Server listening on: {self._host} on port: {self._port}")
            conn, addr = sock.accept()
            self._is_connected = True
            with conn:
                print(f"Connected by ({addr})\n"
                      f"{self._initial_msg}")
                while self._is_connected:
                    self._get_client_data(conn)

                    # Server shuts down if client leaves connection
                    if not self._is_connected:
                        conn.close()
                        break

                    # Print some instructions for the server once the
                    # client sends the first message.
                    if self._is_first_reply and not self._hangman_started:
                        print(self._instrux)
                        self._is_first_reply = False

                    self._send_data(conn)
                # conn.close()


if __name__ == '__main__':
    new_server = Server()
    new_server.server_run()
