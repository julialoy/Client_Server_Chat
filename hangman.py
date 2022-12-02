import random
# CITATION:
# WikiHow's Hangman article was consulted for the order of drawing
# the hanged man when a player answers incorrectly and for basic
# gameplay instructions:
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

    def __init__(self):
        self._secret_word = self._word_bank[random.randint(0, len(self._word_bank)-1)]
        self._is_game_over = False
        self._guessed_letters = []
        self._progress = ["_" for _ in self._secret_word]   # _ used since variable not needed
        self._num_wrong_guesses = 0

    def play_game(self):
        while not self._is_game_over:
            print(f"Word to guess: {' '.join(self._progress)}")
            if self._guessed_letters:
                print(f"Letters guessed: {' '.join(self._guessed_letters)}")
            player_guess = input('Guess a letter: ')

            while player_guess.lower() in self._guessed_letters:
                player_guess = input('You already guessed that letter.\nGuess a letter: ')

            while len(player_guess) > 1:
                player_guess = input('You may only guess one letter.\nGuess a letter: ')

            self._guessed_letters.append(player_guess.lower())

            if player_guess.lower() not in self._secret_word:
                self._num_wrong_guesses += 1
                print(self._wrong_guesses[self._num_wrong_guesses-1])
                if self._num_wrong_guesses < 8:
                    print('Sorry! That letter is not in the word.')
                else:
                    print(f"The word was {self._secret_word}.")
                    print('Game Over! You lost!')
                    self._is_game_over = True
            else:
                print('That is a correct guess!')
                for i in range(len(self._secret_word)):
                    if self._secret_word[i] == player_guess.lower():
                        self._progress[i] = self._secret_word[i]

            if "_" not in self._progress:
                self._is_game_over = True
                print(f"The word was {self._secret_word}.")
                print("You won!")

