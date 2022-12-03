from socket import *

from hangman import HangmanGame


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
        self._instrux = "Type a message." \
                        "\nType /f when you are finished sending messages are ready to wait for a response." \
                        "\nType /hangman to start a Hangman game."
        self._quit_msg = "Type /q to quit"
        self._is_connected = False
        self._hangman_started = False
        self._hangman_game = None

    def _get_messages(self, sckt):
        if not self._is_connected:
            return

        server_msg = sckt.recv(1024).decode()
        while server_msg[-2:] != '/f':
            if '/hangman' in server_msg:
                self._hangman_started = True

            if server_msg[-2:] == '/f' and len(server_msg) > 2 and not self._hangman_started:
                print(f"SERVER: {server_msg[:-2]}")
            elif server_msg[-2:] == '/f' and len(server_msg) > 2:
                print(server_msg[:-2])
            elif server_msg[-2:] == '/q':
                self._is_connected = False
                print(f"Server closed connection.")
                break

            if '/endhangman' in server_msg:
                self._hangman_started = False

            if not self._hangman_started:
                print(f"SERVER: {server_msg}")
            elif len(server_msg) > 0 and server_msg != '/hangman':
                print(server_msg)

            server_msg = sckt.recv(1024).decode()

            # elif server_msg == '/hangman':
            #     self._hangman_started = True

    def _send_message(self, sckt):
        if not self._is_connected:
            return

        if self._hangman_started:
            client_msg = input('> ')
            sckt.send(client_msg.encode())

        # if self._hangman_started and not self._hangman_game:
        #     client_msg = '/f'
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

    def send_server_hangman(self, sckt, data):
        data = data
        sckt.send(data.encode())

    def recv_server_hangman(self, sckt):
        server_guess = sckt.recv(1).decode()
        return server_guess

    def play_hangman(self, sckt, player_number=1):
        if player_number == 1:
            new_game = HangmanGame()
            self._hangman_game = new_game

        print(self._hangman_game.instructions)
        self.send_server_hangman(sckt, self._hangman_game.instructions)
        while not self._hangman_game.get_game_over():
            game_progress = self._hangman_game.get_game_progress()
            print(game_progress)
            self.send_server_hangman(sckt, game_progress+'\n')

            guessed_letters = self._hangman_game.get_letters_guessed()
            if guessed_letters:
                print(guessed_letters)
                self.send_server_hangman(sckt, guessed_letters+'\n')

            if self._hangman_game.get_player_turn() == 1:
                self.send_server_hangman(sckt, "CLIENT IS GUESSING")
                client_guess = self._hangman_game.get_player_guess()
                self.send_server_hangman(sckt, f"CLIENT GUESSED {client_guess}")
                game_response = self._hangman_game.get_guess_result(client_guess)
                print(game_response)
                self.send_server_hangman(sckt, game_response+'\n')
            else:
                print("SERVER IS GUESSING")
                self.send_server_hangman(sckt, "Guess a letter: ")
                self.send_server_hangman(sckt, '/f')
                server_guess = self.recv_server_hangman(sckt)
                print(f"SERVER GUESSED {server_guess}")
                game_response = self._hangman_game.get_guess_result(server_guess)
                print(game_response)
                self.send_server_hangman(sckt, game_response+'\n')

            self._hangman_game.advance_turn()

        self._hangman_game = None
        self._hangman_started = False
        self.send_server_hangman(sckt, "******************* GAME OVER *******************************")
        self.send_server_hangman(sckt, '/endhangman')
        self.send_server_hangman(sckt, '/f')

    def client_run(self):
        with socket(AF_INET, SOCK_STREAM) as client_sock:
            client_sock.connect((self._host, self._port))
            self._is_connected = True
            print(self._instrux)
            print(self._quit_msg)
            while self._is_connected:
                self._send_message(client_sock)
                if not self._is_connected:
                    client_sock.close()
                self._get_messages(client_sock)


if __name__ == '__main__':
    new_client = Client()
    new_client.client_run()
