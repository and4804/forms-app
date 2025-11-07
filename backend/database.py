import sqlite3
import json
from datetime import datetime

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect('forms.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_submission(data):
    """Save form submission to database"""
    conn = sqlite3.connect('forms.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO submissions (name, phone, age, email, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data['phone'],
        data['age'],
        data.get('email', ''),
        datetime.now().isoformat()
    ))
    conn.commit()
    submission_id = cursor.lastrowid
    conn.close()
    return submission_id

def get_all_submissions():
    """Get all submissions from database"""
    conn = sqlite3.connect('forms.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions ORDER BY timestamp DESC')
    columns = [description[0] for description in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results

def get_submission_count():
    """Get total number of submissions"""
    conn = sqlite3.connect('forms.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM submissions')
    count = cursor.fetchone()[0]
    conn.close()
    return count
