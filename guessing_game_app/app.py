from flask import Flask, request, render_template, redirect, url_for, session, flash
import random
import sqlite3

app = Flask(__name__)  # Flask app
app.secret_key = "this is a secret key"

# Global variables to store game data
target_number = random.randint(1, 100)  # Generate a random target number between 1 and 100
guesses = 0  # Initialize the number of guesses to 0
total_guesses = 0  # Initialize the total number of guesses to 0
game_played = 0  # Initialize the number of games played to 0

def init_db():
    conn = sqlite3.connect('users.db')  # connects to the database
    cursor = conn.cursor()  # creates a cursor object to interact with the database using SQL commands
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    conn.commit()  # commits the change to the database
    conn.close()  # closes the connection to the database to free up resources/memory

@app.route("/home", methods=["GET", "POST"])
def home():
    global target_number, guesses, total_guesses, game_played
    if 'users' not in session:
        flash('Please login/signup')
        return redirect('/')

    if 'users' in session:
        user = session['users']
    if request.method == "POST":

            # Get user's guess from the form
            try:
                user_guess = int(request.form.get("guess", 0))
            except ValueError:
                return render_template('index.html', error="Please enter a valid number.", user=session.get('username'))
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
                attempts = guesses
                number = target_number
                # Reset the game
                target_number = 1
                guesses = 0
                return render_template('index.html', message=message, game_over=True, attempts=attempts, number=number, user=user)
    # game over function give the play again function if the game_over equal to ture
            # Check if the user's guess is too high or too low
            elif user_guess < target_number:
                message = "Too low!"
            else:
                message = "Too high!"

            return render_template('index.html', message=message, user=user)

    # For GET requests, display the default page
    return render_template('index.html', user=session.get('users'))

@app.route("/copyright", methods=["GET"])
def copyright():
    return render_template('copyright.html')

@app.route("/leaderboard", methods=["GET", "POST"])
def leaderboard():
    return render_template('leaderboard.html')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    pass

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            flash("sucessfully registered")
            return redirect(url_for('login'))


        except sqlite3.IntegrityError:
            error = 'An error occurred during registration/username already exist.'
            return render_template('register.html', error=error)

    return render_template('register.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password =?', (username,password))
        users = cursor.fetchone()
        print(users)
        conn.close()
        if users and password:  # Check user and hashed password and the plain password is correct.
            session['users'] = users[1]  # session the user
            return redirect('/home')  # return to welcome page
        else:
            flash('Username or Password Incorrect')  # flash the error message
            return redirect(url_for('login'))  # reload the login page to allow user to login again.
    return render_template('login.html')
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('users', None)
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)  # run the flask app in debug mod
