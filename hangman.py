import random
import os
import time
from words import words

hangman_stages = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\  |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\  |
      /    |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\  |
      / \  |
           |
    =========
    """
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_score(name, level, score):

    scores = {}

    try:

        with open("scores.txt", "r") as file:

            lines = file.readlines()

            current_player = ""

            for line in lines:

                line = line.strip()

                if line.startswith("Player:"):

                    current_player = line.replace("Player: ", "")

                    scores[current_player] = {
                        "easy": 0,
                        "medium": 0,
                        "hard": 0
                    }

                elif line.startswith("Easy:"):

                    scores[current_player]["easy"] = int(
                        line.replace("Easy: ", "")
                    )

                elif line.startswith("Medium:"):

                    scores[current_player]["medium"] = int(
                        line.replace("Medium: ", "")
                    )

                elif line.startswith("Hard:"):

                    scores[current_player]["hard"] = int(
                        line.replace("Hard: ", "")
                    )

    except FileNotFoundError:
        pass

    if name not in scores:

        scores[name] = {
            "easy": 0,
            "medium": 0,
            "hard": 0
        }

    if score > scores[name][level]:

        scores[name][level] = score

    with open("scores.txt", "w") as file:

        for player, player_scores in scores.items():

            file.write(f"Player: {player}\n")

            if player_scores["easy"] > 0:
                file.write(f"Easy: {player_scores['easy']}\n")

            if player_scores["medium"] > 0:
                file.write(f"Medium: {player_scores['medium']}\n")

            if player_scores["hard"] > 0:
                file.write(f"Hard: {player_scores['hard']}\n")

            file.write("-" * 30 + "\n")

def show_scores():

    clear()

    print("=" * 40)
    print("🏆 LEADERBOARD 🏆")
    print("=" * 40)

    try:

        with open("scores.txt", "r") as file:

            content = file.read()

            if content.strip() == "":
                print("\nNo scores available.")

            else:
                print(content)

    except FileNotFoundError:

        print("\nNo scores available.")

    input("\nPress Enter To Continue...")

def loading_screen():

    clear()

    print("\n🎮 Starting Hangman Game", end="")

    for i in range(5):

        print(".", end="", flush=True)

        time.sleep(0.3)

    time.sleep(0.5)

def play_game():

    clear()

    print("=" * 50)
    print("🎮 WELCOME TO HANGMAN GAME 🎮")
    print("=" * 50)

    name = input("\nEnter Your Name: ").title()

    print("\nSelect Difficulty")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    choice = input("\nChoose (1/2/3): ")

    if choice == "1":

        level = "easy"

    elif choice == "2":

        level = "medium"

    elif choice == "3":

        level = "hard"

    else:

        print("\n⚠ Invalid Choice")

        time.sleep(1.5)

        return

    word = random.choice(words[level])

    guessed_letters = []

    wrong_guesses = 0

    max_attempts = 6

    score = 100

    hint_used = False

    message = ""

    while wrong_guesses < max_attempts:

        clear()

        print("=" * 50)
        print(f"🎯 Difficulty: {level.upper()}")
        print("=" * 50)

        print(hangman_stages[wrong_guesses])

        display_word = ""

        for letter in word:

            if letter in guessed_letters:

                display_word += letter + " "

            else:

                display_word += "_ "

        print("\n📝 Word:", display_word)

        print("\n🔤 Guessed Letters:", " ".join(guessed_letters))

        print(f"\n❤️ Remaining Attempts: {max_attempts - wrong_guesses}")

        print(f"⭐ Score: {score}")

        if message != "":

            print(f"\n{message}")

        if "_" not in display_word:

            print("\n🎉 Congratulations! You Won!")

            print(f"\n🏆 Final Score: {score}")

            save_score(name, level, score)

            input("\nPress Enter To Continue...")

            break

        print("\nOptions")
        print("1. Guess Letter")
        print("2. Use Hint (-20 Score)")

        option = input("\nChoose Option: ")

        if option == "2":

            if not hint_used:

                remaining_letters = []

                for letter in word:

                    if letter not in guessed_letters:

                        remaining_letters.append(letter)

                hint = random.choice(remaining_letters)

                guessed_letters.append(hint)

                hint_used = True

                score = max(0, score - 20)

                message = f"💡 Hint Letter: {hint}"

                continue

            else:

                message = "⚠ Hint Already Used"

                continue

        guess = input("\nEnter A Letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():

            message = "⚠ Please Enter A Valid Single Letter"

            continue

        if guess in guessed_letters:

            message = "⚠ Letter Already Guessed"

            continue

        guessed_letters.append(guess)

        if guess in word:

            message = "✅ Correct Guess!"

        else:

            message = "❌ Incorrect Guess!"

            wrong_guesses += 1

            score = max(0, score - 10)

    else:

        clear()

        print(hangman_stages[6])

        print("\n💀 GAME OVER 💀")

        print(f"\nThe Correct Word Was: {word}")

        print(f"\n🏆 Final Score: {score}")

        save_score(name, level, score)

        input("\nPress Enter To Continue...")

while True:

    loading_screen()

    clear()

    print("=" * 50)
    print("🎮 HANGMAN GAME 🎮")
    print("=" * 50)

    print("\n1. Play Game")
    print("2. View Leaderboard")
    print("3. Exit")

    menu = input("\nEnter Choice: ")

    if menu == "1":

        play_game()

    elif menu == "2":

        show_scores()

    elif menu == "3":

        print("\n👋 Thanks For Playing!")

        break

    else:

        print("\n⚠ Invalid Choice")

        time.sleep(1.5)