import sqlite3
from flask import Flask, render_template, g #global holding space for db

app = Flask(__name__)

def get_db_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('shinhackers.db')
    return db

@app.teardown_appcontext #automatically close the database
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/translate')
def translate():
    db = get_db_connection()
    a = db.execute("SELECT * FROM Games WHERE Month = 4").fetchall()
    a_result = a
    b = db.execute("SELECT Team, Ours, Theirs FROM Games WHERE Ours > Theirs").fetchall()
    b_result = b
    c = db.execute("SELECT * FROM Games").fetchall()
    c_result = c
    d = db.execute("SELECT Day, Month, Team FROM Games WHERE Ours > Theirs AND Month = 5").fetchall()
    if d:
        d_result = d
    else:
        d_result = "None"
    e = db.execute("SELECT Ours, Theirs FROM Games WHERE Team = 'Bellyfloppers' OR Team = 'Kneeknockers'").fetchall()
    e_result = e
    f = db.execute("SELECT COUNT(*) FROM Games WHERE Ours > Theirs").fetchone()[0]
    f_result = f
    g = db.execute("SELECT MAX(Ours-Theirs) FROM Games").fetchone()[0]
    g_result = g
    h = db.execute("SELECT * FROM Games ORDER BY Month, Day").fetchall()
    h_result = h

    return render_template('translate.html',
                    a=a_result,
                    b=b_result,
                    c=c_result,
                    d=d_result,
                    e=e_result,
                    f=f_result,
                    g=g_result,
                    h=h_result)





if __name__ == '__main__':
    app.run(debug=True, port=5003)