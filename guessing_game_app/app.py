from flask import Flask, request, render_template, redirect, url_for, session
import random

app = Flask(__name__) #flask app
app.secret_key = "this is a sceret key:"
#create Global variables to store game data
target_number = random.randint(1, 100) # generate a random target number between 0 and 100
guesses = 0 # initialise the number of guesses to 0
total_guesses = 0 # initialise the total number of guesses to 0
game_played = 0 # initialise the number of games played to 0

#Define the dafault rout for the web application
@app.route("/", methods=["GET", "POST"])
def home():
    global target_number, guesses, total_guesses, game_played # access the global variables in the function

    #GEt usr's guess from the form
    user_guess = int(request.form.get("guess", 0))
    guesses += 1 # increment the number of guesses by 1

    # Check if th euser's guess is correct
    if user_guess == target_number:
        game_played += 1
        total_guesses += guesses
        average_guesses = total_guesses / game_played
        message = f"Congratulations! You guessed the number in {guesses} attempts. Average guesses {average_guesses:.2f}. Play again?"
        return render_template('index.html', message=message, game_over=True)
    # check if the user's guess is too high or too low
    else:
        if user_guess < target_number:
            message = "too low"
        else:
            message = "too high"
        return render_template('index.html', message=message)

    return render_template('index.html') # render the index.html template

if __name__ == "__main__":
    app.run(debug=True) # run the flask app in debug mode