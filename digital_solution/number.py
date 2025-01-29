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
time = 0
file_path = "digital_solution/number.txt"
history = []

def read_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []
def write_history(file_path, history):
    with open(file_path, "w") as file:
        for numbers in history:
            file.write(f"{numbers}\n")

while guess != number and time <= 10:
    guess = input("Guess the number: ")
    if guess.isdigit():
        guess = int(guess)
        if guess > number:
            print("Too high")
            time = time + 1
        elif guess < number:
            print("Too low")
            time = time + 1

if guess == number:
    print("You win!")
    history.append(number)
elif guess != number:
    print("Game over!")
    print("The number was: ", number)
    history.append(number)

write_history(file_path, history)