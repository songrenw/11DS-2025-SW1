from flask import Flask, request, render_template
import random

app = Flask(__name__)  # Flask app
app.secret_key = "this is a secret key"

# Global variables to store game data
target_number = random.randint(0, 100)  # Generate a random target number between 1 and 100
guesses = 0  # Initialize the number of guesses to 0
total_guesses = 0  # Initialize the total number of guesses to 0
game_played = 0  # Initialize the number of games played to 0

@app.route("/", methods=["GET", "POST"])
def home():
    global target_number, guesses, total_guesses, game_played

    if request.method == "POST":
        # Get user's guess from the form
        try:
            user_guess = int(request.form.get("guess", 0))
        except ValueError:
            return render_template('index.html', error="Please enter a valid number.")
        guesses += 1  # Increment the number of guesses by 1

        # Check if the user's guess is correct
        if user_guess == target_number:
            game_played += 1
            total_guesses += guesses
            average_guesses = total_guesses / game_played
            message = (
                f"Congratulations! You guessed the number in {guesses} attempts. "
                f"Average guesses: {average_guesses:.2f}. Play again?"
            )
            # Reset the game
            target_number = random.randint(1, 100)
            guesses = 0
            return render_template('index.html', message=message, game_over=True)

        # Check if the user's guess is too high or too low
        elif user_guess < target_number:
            message = "Too low!"
        else:
            message = "Too high!"

        return render_template('index.html', message=message)

    # For GET requests, display the default page
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) # run the flask app in debug mode