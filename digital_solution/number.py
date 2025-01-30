# guess the number game
# create a random number between 1 and 100
# ask the user to guess the number
# if the user's guess is higher than the random number, say "too high"
# if the user's guess is lower than the random number, say "too low"
# if the user's guess is equal to the random number, say "you win!"
# if the user's guess is not a number, say "please enter a number"

import random
import os
number = random.randint(1, 100)
guess = 0
attempt = 0
max_attempt = 10
file_path = "number.txt"
history = []
low = 1
high = 100
trys = 0


def read_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []
def write_history(file_path, history):
    with open(file_path, "w") as file:
        for entry in history:
            file.write(f"{entry}\n")

history = read_history(file_path)

while attempt < max_attempt:
    try:
        tips = random.randint(low, high)
        guess = input(f"Attempt: {attempt +1} Guess the number(Try:{tips}): ")
        if guess.isdigit():
            guess = int(guess)
            attempt += 1
            if guess > number:
                print("Too high")
                high = guess - 1
            elif guess < number:
                print("Too low")
                low = guess + 1
            else:
                print("You win!")
                history.append(f"Win: {trys + 1}")
                write_history(file_path, history)
                break
        else:
            print("Please enter a valid number")
    except ValueError:
        print("Invalid input. Please enter a number.")


if guess != number:
    print("Game over!")
    print(f"The number was:{number}")
    history.append(f"Lose: {trys + 1}")
    write_history(file_path, history)

print('\ngame over:')
for entry in history:
    print(entry)