import sqlite3

def delete_lab_work_table():
    """Delete the LabWork table from the database."""
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    try:
        # Drop the LabWork table if it exists
        cursor.execute("DROP TABLE IF EXISTS LabWork")
        conn.commit()
        print("LabWork table deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting the LabWork table: {e}")
    finally:
        conn.close()

# Call the function to delete the LabWork table
delete_lab_work_table()