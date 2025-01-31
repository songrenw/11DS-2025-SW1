# guess the number game
# create a random number between 1 and 100
# ask the user to guess the number
# if the user's guess is higher than the random number, say "too high"
# if the user's guess is lower than the random number, say "too low"
# if the user's guess is equal to the random number, say "you win!"
# if the user's guess is not a number, say "please enter a number"
# create a batabase for each number(1 to 100)
# create a table for each number
# create a column for each attempt
# insert the number and the attempt into the database
import random
import os
import sqlite3

number = random.randint(1, 100)
guess = 0
attempt = 0
file_path = "number1.txt"
history = []
low = 1
high = 100

def init_db():
    conn = sqlite3.connect('number.db')  # connects to the datebase
    cursor = conn.cursor()  # creats a cursor object to interact with the database using SQL commands
    # cursor.execute() is used to execute SQL commands
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER UNIQUE NOT NULL,
                attempt INTEGER NOT NULL
            )
        ''')
    conn.commit()  # commits the change to the database
    conn.close()  # closes the connection to the database to free up resources/memory

def insert_db(number, attempt):
    conn = sqlite3.connect('number.db')
    cursor = conn.cursor()
    cursor.execute('SELECT attempt FROM users WHERE number = ?', (number,))
    data = cursor.fetchone()

    if data:
        current_attempts = data[0]
        new_avg = (current_attempts + attempt) / 2
        cursor.execute('UPDATE users SET attempt = ? WHERE number = ?', (new_avg, number))
    else:
        cursor.execute('INSERT INTO users (number, attempt) VALUES (?, ?)', (number, attempt))
    conn.commit()
    conn.close()

def tips(low, high):
    if high == low:
        return high
    return (high + low) // 2

init_db()
print(f"Welcome to the number guessing game. You have to guess a number between 1 and 100.")
while guess != number:
    try:
        tip = tips(low, high)
        guess = input(f"Attempt: {attempt + 1}, Guess the number (Try: {tip}): ")
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
                insert_db(number, attempt)
                replay = input("Do you want to play again? (y/n): ").lower()
                if replay == "y":
                    number = random.randint(1, 100)
                    guess = 0
                    attempt = 0
                    low = 1
                    high = 100
                    trys += 1
                else:
                    break
        else:
            print("Please enter a valid number")
    except ValueError:
        print("Invalid input. Please enter a number.")

print('game over:')
conn = sqlite3.connect('number.db')
cursor = conn.cursor()
cursor.execute('SELECT number, attempt FROM users')
datas = cursor.fetchall()
if datas:
    for data in datas:
        print(f"Number: {data[0]} Attempt: {data[1]}")
conn.close()



