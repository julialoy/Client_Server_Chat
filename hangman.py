import random


# CITATION:
# WikiHow's Hangman article was consulted for the order of drawing
# the hanged man when a player answers incorrectly and for basic
# gameplay instructions:
# WikiHow. (Nov. 30, 2022). "Play Hangman."
# https://www.wikihow.com/Play-Hangman
class HangmanGame:
    """
    Creates a game of Hangman. There is at least one human player and the computer.
    The computer will select a random word from the word bank and the players
    must guess the word before the drawing of the hanged man is completed.
    Each incorrect guess adds another part to the drawing of the hanged man.
    If either player guesses correctly before the drawing is complete,
    that player wins. If neither player guesses correctly before the drawing is
    complete, both players lose.
    """
    # Strings showing the gradual progression of drawing the Hanged Man
    # when players guess incorrectly
    _first_wrong = "  ____\n" + "      |\n" + "      |\n" + "      |\n" + "      |\n"
    _second_wrong = "  ____\n" + "      |\n" + " 0    |\n" + "      |\n" + "      |\n"
    _third_wrong = "  ____\n" + "      |\n" + " 0    |\n" + " |    |\n" + "      |\n"
    _fourth_wrong = "  ____\n" + "      |\n" + " 0    |\n" + "/|    |\n" + "      |\n"
    _fifth_wrong = "  ____\n" + "      |\n" + " 0    |\n" + "/|\   |\n" + "      |\n"
    _sixth_wrong = "  ____\n" + "      |\n" + " 0    |\n" + "/|\   |\n" + "/     |\n"
    _seventh_wrong = "  ____\n" + "      |\n" + " 0    |\n" + "/|\   |\n" + "/ \   |\n"
    _eighth_wrong = "  ____\n" + " |    |\n" + " 0    |\n" + "/|\   |\n" + "/ \   |\n"
    _wrong_guesses = [
        _first_wrong, _second_wrong, _third_wrong, _fourth_wrong,
        _fifth_wrong, _sixth_wrong, _seventh_wrong, _eighth_wrong
    ]
    # Word bank, game instructions, and game over message
    _word_bank = [
        "banana",
        "computer",
        "network",
        "mouse",
        "light",
        "notebook",
        "pencil",
        "swimming",
        "blanket"
    ]
    _instructions = ("******************* HANGMAN *******************************\n"
                    "A random word will be selected by the game. The length \n"
                    "will be indicated by blanks. You will take turns guessing, \n"
                    "only guessing when prompted. If you and your partner correctly \n"
                    "guess the secret word before the drawing of the Hanged Man is complete, \n"
                    "you both win! But if you don't guess correctly before the drawing is complete \n"
                    "you both lose. Good luck!\n" \
                    "**********************************************************\n")
    _game_over = ("******************* GAME OVER *******************************")

    def __init__(self, conn, player_one, player_two):
        self._secret_word = self._word_bank[random.randint(0, len(self._word_bank)-1)]
        self._is_game_over = False
        self._guessed_letters = []
        self._progress = ["_" for _ in self._secret_word]
        self._num_wrong_guesses = 0
        self._player_one = player_one
        self._player_two = player_two
        self._player_turn = 1       # The player initiating the game is always player 1
        self._connection = conn

    def get_game_over(self):
        """Returns game state."""
        return self._is_game_over

    def get_letters_guessed(self):
        """Returns the letters already guessed as a space-separated string."""
        if self._guessed_letters:
            return f"Letters guessed: {' '.join(self._guessed_letters)}"

    def get_player_guess(self, player):
        """Retrieves a player's guess, ensures the guess is only 1 letter
        and is not a duplicate guess, adds the guess to the _guessed_letters
        list and returns the guess.
        """
        if player == self._player_one:
            player_guess = input("Guess a letter: \n> ")
        else:
            self.send_hangman("Guess a letter: \n")
            self.send_hangman('/f')
            player_guess = self.recv_hangman()

        while player_guess.lower() in self._guessed_letters:
            if player == self._player_one:
                player_guess = input(
                    "You already guessed that letter.\nGuess a letter: ")
            else:
                self.send_hangman("You already guessed that letter.\nGuess a letter: \n")
                self.send_hangman('/f')
                player_guess = self.recv_hangman()

        # while len(player_guess) > 1:
        #     player_guess = input(
        #         'You may only guess one letter.\nGuess a letter: ')

        self._guessed_letters.append(player_guess.lower())

        return player_guess

    def get_game_progress(self):
        """Returns the current state of the word to guess, with letters filled
        in if they have been guessed and unguessed letters as blanks.
        """
        return f"Word to guess: {' '.join(self._progress)}"

    def get_guess_result(self, guess=None):
        """Evaluates the player's guess to determine whether it was a
        correct or incorrect guess, then updates the game progress and
        game state.
        """
        player_guess = self._guessed_letters[-1] if not guess else guess
        if player_guess not in self._secret_word:
            self._num_wrong_guesses += 1
            # print(self._wrong_guesses[self._num_wrong_guesses - 1])
            if self._num_wrong_guesses < 8:
                return (f"{self._wrong_guesses[self._num_wrong_guesses - 1]}\n"
                        f"Sorry! That letter is not in the word.")
            else:
                self._is_game_over = True
                return (f"{self._wrong_guesses[self._num_wrong_guesses - 1]}\n"
                        f"The word was {self._secret_word}.\n"
                        f"Game Over! You lost!")
        else:
            for i in range(len(self._secret_word)):
                if self._secret_word[i] == player_guess.lower():
                    self._progress[i] = self._secret_word[i]
            if ''.join(self._progress) == self._secret_word:
                self._is_game_over = True
                return f"Congratulations! You won!"

            return "That is a correct guess!"

    def get_player_turn(self):
        """Returns the number of the player who is currently allowed
        to guess.
        """
        return self._player_turn

    def advance_turn(self):
        """Advances the gameplay to the next player."""
        self._player_turn = 2 if self._player_turn == 1 else 1

    def send_hangman(self, data):
        data = data
        self._connection.sendall(data.encode())

    def recv_hangman(self):
        guess = self._connection.recv(1).decode()
        return guess

    def play_hangman(self):
        # if player_number == 1:
        #     new_game = HangmanGame()
        #     self._hangman_game = new_game

        print(self._instructions)
        self.send_hangman('\n'+self._instructions+'\n')
        while not self.get_game_over():
            game_progress = self.get_game_progress()
            print(game_progress)
            self.send_hangman(game_progress+'\n')

            guessed_letters = self.get_letters_guessed()
            if guessed_letters:
                print(guessed_letters)
                self.send_hangman(guessed_letters+'\n')

            if self.get_player_turn() == 1:
                self.send_hangman(f"{self._player_one} IS GUESSING")
                player_one_guess = self.get_player_guess(self._player_one)
                self.send_hangman(f"{self._player_one} GUESSED {player_one_guess}")
                game_response = self.get_guess_result(player_one_guess)
                print(game_response)
                self.send_hangman(game_response)
            else:
                print(f"{self._player_two} IS GUESSING")
                player_two_guess = self.get_player_guess(self._player_two)
                print(f"{self._player_two} GUESSED {player_two_guess}")
                game_response = self.get_guess_result(player_two_guess)
                print(game_response)
                self.send_hangman(game_response)

            self.advance_turn()

        # self._hangman_game = None
        # self._hangman_started = False
        print(self._game_over)
        self.send_hangman(self._game_over)
        self.send_hangman('/endhangman')
        self.send_hangman('/f')

    #
    # def send_hangman_info(self, info):
    #     self._connection.send(info.encode())
    #
    # def get_hangman_info(self):
    #     self._connection.recv(1024)
    #
    # def play_game(self):
    #     while not self._is_game_over:
    #         current_progress = f"Word to guess: {' '.join(self._progress)}"
    #         print(current_progress)
    #         self.send_hangman_info(current_progress)
    #
    #         if self._guessed_letters:
    #             current_guessed = f"Letters guessed: {' '.join(self._guessed_letters)}"
    #             print(current_guessed)
    #             self.send_hangman_info(current_guessed)
    #
    #         self.send_hangman_info("OTHER PLAYER IS GUESSING")
    #         player_guess = input('Guess a letter: ')
    #
    #         while player_guess.lower() in self._guessed_letters:
    #             player_guess = input('You already guessed that letter.\nGuess a letter: ')
    #
    #         while len(player_guess) > 1:
    #             player_guess = input('You may only guess one letter.\nGuess a letter: ')
    #
    #         self._guessed_letters.append(player_guess.lower())
    #         self.send_hangman_info(f"OTHER PLAYER GUESSED {player_guess.lower()}")
    #
    #         if player_guess.lower() not in self._secret_word:
    #             self._num_wrong_guesses += 1
    #             print(self._wrong_guesses[self._num_wrong_guesses-1])
    #             if self._num_wrong_guesses < 8:
    #                 response = 'Sorry! That letter is not in the word.'
    #             else:
    #                 print(f"The word was {self._secret_word}.")
    #                 print('Game Over! You lost!')
    #                 self._is_game_over = True
    #         else:
    #             print('That is a correct guess!')
    #             for i in range(len(self._secret_word)):
    #                 if self._secret_word[i] == player_guess.lower():
    #                     self._progress[i] = self._secret_word[i]
    #
    #         if "_" not in self._progress:
    #             self._is_game_over = True
    #             print(f"The word was {self._secret_word}.")
    #             print("You won!")

