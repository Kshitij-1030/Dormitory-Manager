import sqlite3

def initialize_database():
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT)''')
    conn.commit()
    conn.close()

def insert_user(username, password):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def is_username_exists(username):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0
