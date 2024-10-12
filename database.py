import sqlite3

def create_database(db_name):
    """Create a database and tables if they don't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create Classrooms table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Classrooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        classroom_name TEXT
    )
    """)

    # Create Teachers table with correct columns (bps_grade and specialization)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_name TEXT,
        bps_grade TEXT,
        specialization TEXT
    )
    """)

    # Create Courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        course_code TEXT,
        credits INTEGER
    )
    """)

    # Create Programs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Programs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT,
        semester TEXT
    )
    """)

    # Create Days table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Days (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_name TEXT
    )
    """)

    conn.commit()
    conn.close()

def fetch_data(query):
    """Fetch data from the database."""
    conn = sqlite3.connect("timetable.db")  # Ensure correct database is used
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def execute_query(query, parameters=()):
    """Execute a query to modify the database (INSERT, UPDATE, DELETE)."""
    conn = sqlite3.connect("timetable.db")  # Ensure correct database is used
    cursor = conn.cursor()
    try:
        cursor.execute(query, parameters)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        conn.close()
