import sqlite3

def init_db():
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu_usage REAL NOT NULL,
            memory_usage REAL NOT NULL,
            disk_usage REAL NOT NULL
        )
    ''')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.commit()
    conn.close()

def insert_metrics(timestamp, cpu_usage, memory_usage, disk_usage):
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO metrics (timestamp, cpu_usage, memory_usage, disk_usage)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, cpu_usage, memory_usage, disk_usage))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM metrics ORDER BY id DESC LIMIT 60')
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]

def register_user(username, password_hash):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
    ''', (username, password_hash))
    conn.commit()
    conn.close()

def get_username_by_username(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    rows = cursor.fetchone()
    conn.close()
    return rows
