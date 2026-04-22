import mysql.connector
import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Preet@2004",  # Replace with your MySQL password
        database="attendance_system_1"
    )

def create_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Preet@2004"
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_system_1")
    db.close()

def create_tables():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(100)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            rollno VARCHAR(20),
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(15),
            department VARCHAR(50)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            date DATE,
            time TIME,
            status ENUM('Present', 'Absent'),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );
    """)
 # week 3:
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    db.commit()
    db.close()

# NEW FUNCTION OF WEEK 3 - Database Authentication
def verify_user_credentials(username, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    db.close()
    return result is not None

# NEW FUNCTION FOR WEEK 4 - Add Student to Database
def add_student(name, email, phone, department, rollno):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO students (rollno, name, email, phone, department) VALUES (%s, %s, %s, %s, %s)",
        (rollno, name, email, phone, department)
    )
    db.commit()
    db.close()
    print(f"Student {name} added to database with rollno: {rollno}")

# NEW FUNCTION FOR WEEK 4 - Get Student Info
def get_student_info(rollno):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students WHERE rollno = %s", (rollno,))
    result = cursor.fetchone()
    db.close()
    return result

# WEEK 7 OPTIONAL: Check if attendance already marked today
def is_attendance_marked_today(rollno):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT student_id FROM students WHERE rollno = %s
    """, (rollno,))
    result = cursor.fetchone()
    
    if result:
        student_id = result[0]
        today = datetime.datetime.now().date()
        cursor.execute("""
            SELECT attendance_id FROM attendance 
            WHERE student_id = %s AND date = %s
        """, (student_id, today))
        marked = cursor.fetchone() is not None
        db.close()
        return marked
    db.close()
    return False

# NEW FUNCTION FOR WEEK 6 - Insert Attendance Record
def insert_attendance_record(rollno, status="Present"):
    db = connect_db()
    cursor = db.cursor()
    # Get student_id from roll number
    cursor.execute("SELECT student_id FROM students WHERE rollno = %s", (rollno,))
    result = cursor.fetchone()
    if result:
        student_id = result[0]
        now = datetime.datetime.now()
        date = now.date()
        time = now.time()
        cursor.execute(
            "INSERT INTO attendance (student_id, date, time, status) VALUES (%s, %s, %s, %s)",
            (student_id, date, time, status)
        )
        db.commit()
    db.close()