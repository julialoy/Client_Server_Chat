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
        # self._client_port = 3478
        self._instrux = ("Type a message.\n"
                         "  * Type /f after sending the messages you wish to send.\n"
                         "  * Type /hangman to start a Hangman game.\n"
                         "  * Type /q to quit.")
        self._is_connected = False
        self._hangman_started = False
        self._hangman_game = None

    def _get_messages(self, sckt):
        """Handles retrieving any messages from the server."""
        if not self._is_connected:
            return

        server_msg = sckt.recv(1024).decode()
        # CITATION:
        # Use of delimiter to indicate when server has finished sending
        # messages is based on information in
        # McMillan, G. (Nov. 30, 2022). "Socket Programming
        # HOWTO" in Python documentation. [Python docs v. 3.4.10]
        # https://docs.python.org/3.4/howto/sockets.html
        while server_msg[-2:] != '/f':
            if '/hangman' in server_msg:
                self._hangman_started = True

            if server_msg[-2:] == '/f' and len(server_msg) > 2 and not self._hangman_started:
                print(f"SERVER: {server_msg[:-2]}")
            elif server_msg[-2:] == '/f' and len(server_msg) > 2:
                print(server_msg[:-2])
            elif server_msg[-2:] == '/q':
                self._is_connected = False
                print("Server closed connection.")
                break

            if '/endhangman' in server_msg:
                self._hangman_started = False

            # Format output based on game vs. chat
            if not self._hangman_started:
                print(f"SERVER: {server_msg}")
            elif len(server_msg) > 0 and server_msg != '/hangman':
                print(server_msg)

            server_msg = sckt.recv(1024).decode()

            # elif server_msg == '/hangman':
            #     self._hangman_started = True

    def _send_message(self, sckt):
        """Handles sending messages to the server."""
        if not self._is_connected:
            return

        # Hangman game is turn based, client will only enter one input
        if self._hangman_started:
            client_msg = input('> ')
            sckt.send(client_msg.encode())

        # When not playing Hangman, client can send as many messages as
        # desired
        while not self._hangman_started:
            client_msg = input('> ')
            sckt.send(client_msg.encode())
            if client_msg == "/q":
                print(f"Closing connection")
                self._is_connected = False
                break
            elif client_msg[-2:] == '/f':
                break
            elif client_msg == '/hangman':
                self._hangman_started = True
                self.play_hangman(sckt)
                break

    def play_hangman(self, sckt):
        new_game = HangmanGame(sckt, "CLIENT", "SERVER")
        new_game.play_hangman()
        self._hangman_started = False
    # def send_server_hangman(self, sckt, data):
    #     data = data
    #     sckt.send(data.encode())
    #
    # def recv_server_hangman(self, sckt):
    #     server_guess = sckt.recv(1).decode()
    #     return server_guess
    #
    # def play_hangman(self, sckt, player_number=1):
    #     if player_number == 1:
    #         new_game = HangmanGame()
    #         self._hangman_game = new_game
    #
    #     print(self._hangman_game.instructions)
    #     self.send_server_hangman(sckt, self._hangman_game.instructions)
    #     while not self._hangman_game.get_game_over():
    #         game_progress = self._hangman_game.get_game_progress()
    #         print(game_progress)
    #         self.send_server_hangman(sckt, game_progress+'\n')
    #
    #         guessed_letters = self._hangman_game.get_letters_guessed()
    #         if guessed_letters:
    #             print(guessed_letters)
    #             self.send_server_hangman(sckt, guessed_letters+'\n')
    #
    #         if self._hangman_game.get_player_turn() == 1:
    #             self.send_server_hangman(sckt, "CLIENT IS GUESSING")
    #             client_guess = self._hangman_game.get_player_guess()
    #             self.send_server_hangman(sckt, f"CLIENT GUESSED {client_guess}")
    #             game_response = self._hangman_game.get_guess_result(client_guess)
    #             print(game_response)
    #             self.send_server_hangman(sckt, game_response+'\n')
    #         else:
    #             print("SERVER IS GUESSING")
    #             self.send_server_hangman(sckt, "Guess a letter: ")
    #             self.send_server_hangman(sckt, '/f')
    #             server_guess = self.recv_server_hangman(sckt)
    #             print(f"SERVER GUESSED {server_guess}")
    #             game_response = self._hangman_game.get_guess_result(server_guess)
    #             print(game_response)
    #             self.send_server_hangman(sckt, game_response+'\n')
    #
    #         self._hangman_game.advance_turn()
    #
    #     self._hangman_game = None
    #     self._hangman_started = False
    #     self.send_server_hangman(sckt, "******************* GAME OVER *******************************")
    #     self.send_server_hangman(sckt, '/endhangman')
    #     self.send_server_hangman(sckt, '/f')

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
            print(self._instrux)
            while self._is_connected:
                self._send_message(client_sock)

                # Client shuts down if server leaves connection
                if not self._is_connected:
                    client_sock.close()

                self._get_messages(client_sock)


if __name__ == '__main__':
    new_client = Client()
    new_client.client_run()
