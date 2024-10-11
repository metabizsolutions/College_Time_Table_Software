import sqlite3

def create_database(db_name):
    # Connect to the SQLite database (creates the database if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Table for Programs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Programs (
        program_id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        semester TEXT NOT NULL
    )
    ''')

    # Table for Courses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        course_code TEXT NOT NULL,
        credits TEXT NOT NULL,
        program_id INTEGER,
        FOREIGN KEY(program_id) REFERENCES Programs(program_id)
    )
    ''')

    # Table for Teachers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_name TEXT NOT NULL,
        bps_grade INTEGER NOT NULL,
        specialization TEXT
    )
    ''')

    # Table for Classrooms
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Classrooms (
        classroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
        classroom_name TEXT NOT NULL
    )
    ''')

    # Table for Periods (time slots)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Periods (
        period_id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL
    )
    ''')

    # Table for Days (Weekdays)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Days (
        day_id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_name TEXT NOT NULL
    )
    ''')

    # Table for Schedule (links Courses, Teachers, Classrooms, Periods, and Days)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Schedule (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        teacher_id INTEGER,
        classroom_id INTEGER,
        period_id INTEGER,
        day_id INTEGER,
        program_id INTEGER,
        practical BOOLEAN,
        FOREIGN KEY(course_id) REFERENCES Courses(course_id),
        FOREIGN KEY(teacher_id) REFERENCES Teachers(teacher_id),
        FOREIGN KEY(classroom_id) REFERENCES Classrooms(classroom_id),
        FOREIGN KEY(period_id) REFERENCES Periods(period_id),
        FOREIGN KEY(day_id) REFERENCES Days(day_id),
        FOREIGN KEY(program_id) REFERENCES Programs(program_id)
    )
    ''')

    # Table for Workload (tracks teacher workload)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Workload (
        workload_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        total_hours INTEGER,
        courses_assigned TEXT,
        last_updated DATE,
        FOREIGN KEY(teacher_id) REFERENCES Teachers(teacher_id)
    )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' and tables created successfully!")

if __name__ == "__main__":
    # Create only one database
    create_database("timetable.db")
