# database.py

import sqlite3

def create_database(db_name):
    """Create a database and tables if they don't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Classrooms (
        id INTEGER PRIMARY KEY,
        classroom_name TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        id INTEGER PRIMARY KEY,
        teacher_name TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY,
        course_name TEXT,
        course_code TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Programs (
        id INTEGER PRIMARY KEY,
        program_name TEXT,
        semester TEXT
    )
    """)
    conn.commit()
    conn.close()

def fetch_data(query):
    """Fetch data from the database."""
    conn = sqlite3.connect("timetable.db")  # Adjust database name if needed
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results
