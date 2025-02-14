# guess the number game
# create a random number between 1 and 100
# ask the user to guess the number
# if the user's guess is higher than the random number, say "too high"
# if the user's guess is lower than the random number, say "too low"
# if the user's guess is equal to the random number, say "you win!"
# if the user's guess is not a number, say "please enter a number"
# solving problem
#to made an alugrithum about the average of the number of attempts to guess the number
# create a database for each number(1 to 100)
# create a table for each number
# create a column for each attempt
# insert the number and the attempt into the database
# to make an agluritum that can play the game
# simulate the game using the alugrithum in while try is less than 1000
# bot can simulate the game using the alugrithum(if it too high, the mximum become high, if it too low, the minimum become low and divided by half to guess the next number)
# insert the number and the attempt into the database of the bot
#lambda function is used to calculate the average of the number of attempts to guess the number
#what diffrent between dict, list, and tuple
import random
import sqlite3

number = 100
guess = 0
attempt = 0
low = 1
high = 100
simulation_time = 1000




def init_db():
    conn = sqlite3.connect('number.db')  # connects to the datebase
    cursor = conn.cursor()  # creats a cursor object to interact with the database using SQL commands
    # cursor.execute() is used to execute SQL commands
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS algorithm (
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
    cursor.execute('SELECT attempt FROM algorithm WHERE number = ?', (number,))
    data = cursor.fetchone()

    if data:
        current_attempts = data[0]
        new_avg = round((current_attempts + attempt) / 2, 2) # round to 2 dp
        cursor.execute('UPDATE algorithm SET attempt = ? WHERE number = ?', (new_avg, number))
    else:
        cursor.execute('INSERT INTO algorithm (number, attempt) VALUES (?, ?)', (number, attempt))
    conn.commit()
    conn.close()

def gameover():
    print('game over:')
    conn = sqlite3.connect('number.db')
    cursor = conn.cursor()
    cursor.execute('SELECT number, attempt FROM algorithm')
    datas = cursor.fetchall()
    if datas:
        for data in datas:
            print(f"Number: {data[0]} Attempt: {data[1]}")
    conn.close()

def tips(low, high):
    if high == low:
        return high
    return (high + low) // 2

def simulation_guess(low, high):
    if high == low:
        return high
    midpoint = (high + low) // 2
    range = int((high - low)* 0.05)
    range_adjusted = random.randint(-range, range) # + and - 5% of the midpoint
    return midpoint + range_adjusted

def simulation(low, high):
    number = 100 # generate a new random number every time this function is called
    attempt = 1
    while True:
        simulated_guess = simulation_guess(low, high)
        number_list = [simulated_guess]
        print(number_list, end=" ")
        if simulated_guess > number:
            high = simulated_guess - 1
            attempt += 1

        elif simulated_guess < number:
            low = simulated_guess + 1
            attempt += 1

        else:

            print(f"\nSimulated number: {number}, Simulated attempts: {attempt}")
            insert_db(number, attempt)
            return


init_db()
print("\033[94mWelcome to the number guessing game. You have to guess a number between 1 and 100\033[0m")
clear = input("Do you want to clear the game history? (y/n): ").lower()
if clear == "y":
    conn = sqlite3.connect('number.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM algorithm')
    conn.commit()
    conn.close()
    print("Game history cleared")

chose = input("Do you want to simulate the game using algorithm?(y/n):").lower()
if chose == "y":
    while simulation_time:
        simulation_time = input("How many time would you like to simulate: ")
        if simulation_time.isdigit():
            simulation_time = int(simulation_time)
            while simulation_time > 0:
                simulation(low, high)
                simulation_time -= 1

        else:
            print("Please enter a valid number")

elif chose == "n":
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
                    gameover()
                    replay = input("Do you want to play again? (y/n): ").lower()
                    if replay == "y":
                        number = random.randint(1, 100)
                        guess = 0
                        attempt = 0
                        low = 1
                        high = 100
                    else:
                        break
            else:
                print("Please enter a valid number")
        except ValueError:
            print("Invalid input. Please enter a number.")
else:
    print("Please enter a valid input")



