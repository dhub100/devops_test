import random

DEFAULT_NOUNS = [
    "Tabelle", "Fenster", "Regen", "Wolken", "Server",
    "Adresse", "Muster", "System", "Konsole", "Prozess",
    "Laptop", "Netzwerk", "Kamera", "Ordner", "Schalter",
]


class PoolOfWords:
    """Verwaltet Nomen und liefert ein zufälliges, noch unbenutztes Wort (5–10 Zeichen)."""

    def __init__(self, nouns):
        self._all_nouns = [w.lower() for w in nouns]
        self._used = set()

    def next_word(self):
        candidates = [
            w for w in self._all_nouns
            if w.isalpha() and 5 <= len(w) <= 10 and w not in self._used
        ]
        if not candidates:
            raise RuntimeError("Keine geeigneten neuen Wörter mehr verfügbar.")
        choice = random.choice(candidates)
        self._used.add(choice)
        return choice

    """used_words wie ein Attribut nutzbar, aber nur lesbar"""
    @property
    def used_words(self):
        return sorted(self._used)


class HangmanRound:
    """Verwaltet den Zustand einer einzelnen Hangman-Runde."""
    MAX_ATTEMPTS = 8

    def __init__(self, secret):
        """Initialisiert das Spiel mit dem geheimen Wort."""
        self.secret = secret.lower()
        self.tried_letters = set()
        self.wrong_attempts = 0

    def try_letter(self, letter):
        """Verarbeitet einen einzelnen Buchstabenversuch und gibt True zurück, wenn er im geheimen Wort enthalten."""
        letter = letter.lower()

        if len(letter) != 1 or not letter.isalpha():
            raise ValueError("Please enter exactly one letter (a–z).")

        if letter in self.tried_letters:
            raise ValueError(f"You already tried the letter '{letter}'.")

        self.tried_letters.add(letter)

        if letter in self.secret:
            return True
        else:
            self.wrong_attempts += 1
            return False

    def guess_word(self, attempt):
        """Verarbeitet einen Versuch und gibt True zurück, wenn er mit dem geheimen Wort übereinstimmt."""
        attempt = attempt.lower()

        if not attempt.isalpha():
            raise ValueError("The word must contain only letters.")

        if attempt == self.secret:
            return True
        else:
            self.wrong_attempts += 1
            return False

    def progress_mask(self):
        """ Gibt den aktuellen Fortschritt zurück, z.B. '_ _ r _ _'."""
        return " ".join(c if c in self.tried_letters else "_" for c in self.secret)


class Game:
    """Kontrolliert den Ablauf des Spiels."""
    def __init__(self, word_pool):
        """Nimmt eine PoolOfWords-Instanz entgegen."""
        self.word_pool = word_pool

    def play_one_round(self):
        """Eine komplette Runde Hangman spielen."""
        secret = self.word_pool.next_word()
        game = HangmanRound(secret)

        print(f"\nThe secret word has {len(secret)} letters.")
        print(game.progress_mask())

        while True:
            user_input = input("\nEnter a letter or try the whole word: ").strip()

            try:
                """ Einzelbuchstabe oder ganzes Wort? """
                if len(user_input) == 1:
                    hit = game.try_letter(user_input)
                    if hit:
                        print("Correct.")
                    else:
                        print("Wrong.")
                else:
                    correct = game.guess_word(user_input)
                    if correct:
                        print(f"\nYou won! The word was '{game.secret}'.")
                        break
                    else:
                        print("Wrong word.")

                """ Fortschritt anzeigen und Bedingungen prüfen """
                print("Current progress:", game.progress_mask())
                print("Attempts used:", game.wrong_attempts, "/", game.MAX_ATTEMPTS)

                if game.wrong_attempts >= game.MAX_ATTEMPTS:
                    print(f"\nGame over. The word was '{game.secret}'.")
                    break
                if all(c in game.tried_letters for c in game.secret):
                    print(f"\nYou won! The word was '{game.secret}'.")
                    break

            except ValueError as e:
                print(e)
                continue


def main():
    pool = PoolOfWords(DEFAULT_NOUNS)
    hangman_game = Game(pool)

    while True:
        hangman_game.play_one_round()
        again = input("\nPlay another round? (y/n): ").strip().lower()
        if again != "y":
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()



