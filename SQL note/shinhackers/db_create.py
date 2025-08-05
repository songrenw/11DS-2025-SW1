import sqlite3

conn = sqlite3.connect('shinhackers.db')
cur = conn.cursor()

# Drop
cur.execute('DROP TABLE IF EXISTS Games')


# Create Table
cur.execute("""
CREATE TABLE IF NOT EXISTS Games (
Day INTEGER,
Month INTEGER,
Team TEXT,
Ours INTEGER,
Theirs INTEGER)
""")

# Insert data
game_data = [
    (7, 3, 'Toecrushers', 6, 25),
    (14, 3, 'Headbutters', 0, 10),
    (21, 3, 'Neckwisters', 21, 10),
    (28, 3, 'Ankeltappers', 18, 16),
    (4, 4, 'Armlockers', 0, 6),
    (11, 4, 'Kneeknockers', 0, 9),
    (18, 4, 'Bellyfloppers', 9, 3),
    (25, 4, 'Headbutters', 14, 6),
    (2, 5, 'Toecrushers', 6, 16),
]
cur.executemany('INSERT INTO Games (Day, Month, Team, Ours, Theirs) VALUES (?, ?, ?, ?, ?)', game_data)

conn.commit()
conn.close()