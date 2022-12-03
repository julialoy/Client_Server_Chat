# CITATION:
# Python docs. How to: Socket programming

# CITATION:
# My Python socket project from the beginning of this term
#
# Use of two ports, one for send one for receive, from instructor's
# reply in Ed discussion board:
# https://edstem.org/us/courses/29340/discussion/2175842
from socket import *

from hangman import HangmanGame


class Server:

    def __init__(self):
        self._host = "localhost"
        self._port = 3291
        self._initial_msg = "Waiting for messages..."
        self._instrux = "Type a message.\nType /f when finished sending messages.\nType /hangman to start a Hangman game.\nType /q to quit."
        self._is_first_reply = True
        self._hangman_started = False
        self._is_connected = False
        self._hangman_game = None

    def _get_client_data(self, conn):
        if not self._is_connected:
            return

        client_data = conn.recv(1024).decode()
        while client_data[-2:] != '/f':
            if '/hangman' in client_data:
                self._hangman_started = True

            if client_data[-2:] == '/f' and len(client_data) > 2 and not self._hangman_started:
                print(f"CLIENT: {client_data[:-2]}")
            elif client_data[-2:] == '/f' and len(client_data):
                print(client_data[:-2])
            elif client_data[-2:] == '/q':
                self._is_connected = False
                print("Client left the connection. Closing connection.")
                break

            if '/endhangman' in client_data:
                self._hangman_started = False

            if not self._hangman_started:
                print(f"CLIENT: {client_data}")
            elif len(client_data) > 0 and client_data != '/hangman':
                print(client_data)

            client_data = conn.recv(1024).decode()
            # if client_data[-2:] == '/f' and len(client_data) > 2 and not self._hangman_started:
            #     print(f"CLIENT: {client_data[:-2]}")
            # elif client_data[-2:] == '/f' and len(client_data):
            #     print(client_data[:-2])
            # elif client_data[-2:] == '/q':
            #     self._is_connected = False
            #
            # if '/endhangman' in client_data:
            #     self._hangman_started = False

    def _send_data(self, conn):
        if not self._is_connected:
            return

        if self._hangman_started:
            server_reply = input(' ')
            conn.send(server_reply.encode())

        while not self._hangman_started:
            server_reply = input('> ')
            conn.send(server_reply.encode())
            if server_reply == '/q':
                print(f"Closing connection")
                self._is_connected = False
                break
            elif server_reply[-2:] == '/f':
                break
            elif server_reply == '/hangman':
                self._hangman_started = True
                self.play_hangman(conn)
                break

    def send_client_hangman(self, conn, data):
        data = data
        conn.send(data.encode())

    def recv_client_hangman(self, conn):
        client_guess = conn.recv(1).decode()
        return client_guess

    def play_hangman(self, conn, player_number=1):
        if player_number == 1:
            new_game = HangmanGame()
            self._hangman_game = new_game

        print(self._hangman_game.instructions)
        self.send_client_hangman(conn, self._hangman_game.instructions)
        while not self._hangman_game.get_game_over():
            game_progress = self._hangman_game.get_game_progress()
            print(game_progress)
            self.send_client_hangman(conn, game_progress)

            guessed_letters = self._hangman_game.get_letters_guessed()
            if guessed_letters:
                print(guessed_letters)
                self.send_client_hangman(conn, guessed_letters)

            if self._hangman_game.get_player_turn() == 1:
                self.send_client_hangman(conn, "SERVER IS GUESSING")
                server_guess = self._hangman_game.get_player_guess()
                self.send_client_hangman(conn, f"SERVER GUESSED {server_guess}")
                game_response = self._hangman_game.get_guess_result(server_guess)
                print(game_response)
                self.send_client_hangman(conn, game_response+'\n')
            else:
                print("CLIENT IS GUESSING")
                self.send_client_hangman(conn, "Guess a letter: ")
                self.send_client_hangman(conn, '/f')
                client_guess = self.recv_client_hangman(conn)
                print(f"CLIENT GUESSED {client_guess}")
                game_response = self._hangman_game.get_guess_result(client_guess)
                print(game_response)
                self.send_client_hangman(conn, game_response+'\n')

            self._hangman_game.advance_turn()

        self._hangman_game = None
        self._hangman_started = False
        "******************* GAME OVER *******************************"
        self.send_client_hangman(conn, '/endhangman')
        self.send_client_hangman(conn, '/f')

    def server_run(self):
        with socket(AF_INET, SOCK_STREAM) as sock:
            # Use of setsockopt taken from the project instructions
            # to help avoid "hanging" a port during testing
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((self._host, self._port))
            sock.listen(1)  # Does not connect to multiple clients
            print(f"Server listening on: {self._host} on port: {self._port}")
            conn, addr = sock.accept()
            self._is_connected = True
            with conn:
                print(f"Connected by ({addr})\n"
                      f"{self._initial_msg}")
                while self._is_connected:
                    self._get_client_data(conn)
                    if not self._is_connected:
                        conn.close()
                        break
                    if self._is_first_reply and not self._hangman_started:
                        print(self._instrux)
                        self._is_first_reply = False
                    self._send_data(conn)


if __name__ == '__main__':
    new_server = Server()
    new_server.server_run()
