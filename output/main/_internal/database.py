import sqlite3

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect("timetable.db")

def fetch_query_results(query, params=None):
    """Fetch data from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def delete_record(record_id, table_name):
    """Delete a record from the specified table using the provided ID."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Construct the DELETE SQL query based on the table name
    query = f"DELETE FROM {table_name} WHERE id = ?"
    
    cursor.execute(query, (record_id,))
    conn.commit()
    conn.close()

def update_record(table_name, record_id, updated_data):
    """Update a record in the specified table."""
    conn = connect_db()
    cursor = conn.cursor()

    # Construct the UPDATE SQL query based on the table name
    if table_name == "Classrooms":
        cursor.execute("""
            UPDATE Classrooms
            SET classroom_name = ?
            WHERE classroom_id = ?
        """, (updated_data[0], record_id))

    elif table_name == "Courses":
        cursor.execute("""
            UPDATE Courses
            SET course_name = ?, course_code = ?, credits = ?
            WHERE course_id = ?
        """, (*updated_data, record_id))

    elif table_name == "Programs":
        cursor.execute("""
            UPDATE Programs
            SET program_name = ?, semester = ?
            WHERE program_id = ?
        """, (*updated_data, record_id))

    elif table_name == "Teachers":
        cursor.execute("""
            UPDATE Teachers
            SET teacher_name = ?, bps_grade = ?, specialization = ?
            WHERE teacher_id = ?
        """, (*updated_data, record_id))

    conn.commit()
    conn.close()

def create_database(db_name):
    """Create a database and tables if they don't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Classrooms table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Classrooms (
        classroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
        classroom_name TEXT NOT NULL
    )
    """)

    # Create Teachers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_name TEXT NOT NULL,
        bps_grade TEXT NOT NULL,
        specialization TEXT NOT NULL
    )
    """)

    # Create Courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        course_code TEXT NOT NULL,
        credits INTEGER NOT NULL
    )
    """)

    # Create Programs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Programs (
        program_id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        semester TEXT NOT NULL
    )
    """)

    # Create Days table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Days (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_name TEXT NOT NULL
    )
    """)

    # Updated Timetable table creation
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT,
        semester TEXT,
        teacher TEXT,
        course_title TEXT,
        course_code TEXT,
        classroom TEXT,
        lecture_start_time TEXT,  -- New start time column
        lecture_end_time TEXT,    -- New end time column
        session TEXT
    )
    """)


    
    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Execute a SQL query (INSERT, UPDATE, DELETE)."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()  # Commit changes for INSERT, UPDATE, DELETE
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Add other necessary functions as needed...
if __name__ == "__main__":
    # Call the function to create the database and tables if they don't exist
    create_database("timetable.db")
