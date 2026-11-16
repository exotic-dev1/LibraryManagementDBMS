import sqlite3

DB_NAME = "library.db"


# ================= DATABASE CONNECTION =================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ================= DATABASE INITIALIZATION =================

def initialize_database():
    conn = get_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Books (
                book_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                total_copies INTEGER NOT NULL CHECK(total_copies >= 0),
                available_copies INTEGER NOT NULL
                    CHECK(available_copies >= 0
                    AND available_copies <= total_copies),
                location TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Issue_Records (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL,
                student_id TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT NOT NULL DEFAULT 'ISSUED'
                    CHECK(status IN ('ISSUED', 'RETURNED')),
                FOREIGN KEY (book_id) REFERENCES Books(book_id),
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_issue_student
            ON Issue_Records(student_id)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_issue_book
            ON Issue_Records(book_id)
        """)

        conn.commit()
    finally:
        conn.close()


# ================= BOOK OPERATIONS =================

def add_book(book_id, title, author, genre, copies, location):
    if copies < 0:
        raise ValueError("Number of copies cannot be negative.")

    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO Books
                (book_id, title, author, genre,
                 total_copies, available_copies, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (book_id, title, author, genre, copies, copies, location))
        return "Book added successfully."
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Could not add book: {e}")
    finally:
        conn.close()


def get_books(search=""):
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT * FROM Books
            WHERE book_id LIKE ?
               OR title LIKE ?
               OR author LIKE ?
               OR genre LIKE ?
            ORDER BY title
        """, tuple([f"%{search}%"] * 4)).fetchall()
    finally:
        conn.close()


def update_book(book_id, title, author, genre, location):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute("""
                UPDATE Books
                SET title=?, author=?, genre=?, location=?
                WHERE book_id=?
            """, (title, author, genre, location, book_id))
            if cursor.rowcount == 0:
                raise ValueError("Book not found.")
        return "Book updated successfully."
    finally:
        conn.close()


def delete_book(book_id):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(
                "DELETE FROM Books WHERE book_id=?", (book_id,)
            )
            if cursor.rowcount == 0:
                raise ValueError("Book not found.")
        return "Book deleted successfully."
    except sqlite3.IntegrityError:
        raise ValueError("Cannot delete this book because issue history exists.")
    finally:
        conn.close()


# ================= STUDENT OPERATIONS =================

def add_student(student_id, name, email, phone):
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO Students (student_id, name, email, phone)
                VALUES (?, ?, ?, ?)
            """, (student_id, name, email or None, phone))
        return "Student registered successfully."
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Could not register student: {e}")
    finally:
        conn.close()


def get_students(search=""):
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT * FROM Students
            WHERE student_id LIKE ?
               OR name LIKE ?
               OR email LIKE ?
            ORDER BY name
        """, tuple([f"%{search}%"] * 3)).fetchall()
    finally:
        conn.close()


def update_student(student_id, name, email, phone):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute("""
                UPDATE Students
                SET name=?, email=?, phone=?
                WHERE student_id=?
            """, (name, email or None, phone, student_id))
            if cursor.rowcount == 0:
                raise ValueError("Student not found.")
        return "Student updated successfully."
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Could not update student: {e}")
    finally:
        conn.close()


def delete_student(student_id):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(
                "DELETE FROM Students WHERE student_id=?", (student_id,)
            )
            if cursor.rowcount == 0:
                raise ValueError("Student not found.")
        return "Student deleted successfully."
    except sqlite3.IntegrityError:
        raise ValueError("Cannot delete this student because issue history exists.")
    finally:
        conn.close()


# ================= ISSUE AND RETURN OPERATIONS =================

def issue_book(book_id, student_id):
    conn = get_connection()
    try:
        with conn:
            book = conn.execute("""
                SELECT available_copies FROM Books WHERE book_id=?
            """, (book_id,)).fetchone()

            if book is None:
                raise ValueError("Book not found.")
            if book[0] <= 0:
                raise ValueError("No copies of this book are available.")

            student = conn.execute("""
                SELECT student_id FROM Students WHERE student_id=?
            """, (student_id,)).fetchone()

            if student is None:
                raise ValueError("Student not found.")

            active_issue = conn.execute("""
                SELECT issue_id FROM Issue_Records
                WHERE book_id=? AND student_id=? AND status='ISSUED'
            """, (book_id, student_id)).fetchone()

            if active_issue:
                raise ValueError("This student already has this book.")

            conn.execute("""
                UPDATE Books
                SET available_copies=available_copies-1
                WHERE book_id=? AND available_copies > 0
            """, (book_id,))

            conn.execute("""
                INSERT INTO Issue_Records
                (book_id, student_id, issue_date, due_date, status)
                VALUES (?, ?, date('now'), date('now', '+7 days'), 'ISSUED')
            """, (book_id, student_id))

        return "Book issued successfully. Due date is 7 days from today."
    finally:
        conn.close()


def return_book(book_id, student_id):
    conn = get_connection()
    try:
        with conn:
            issue = conn.execute("""
                SELECT issue_id FROM Issue_Records
                WHERE book_id=? AND student_id=? AND status='ISSUED'
                ORDER BY issue_id DESC LIMIT 1
            """, (book_id, student_id)).fetchone()

            if issue is None:
                raise ValueError("No active issue record found.")

            conn.execute("""
                UPDATE Issue_Records
                SET return_date=date('now'), status='RETURNED'
                WHERE issue_id=?
            """, (issue[0],))

            conn.execute("""
                UPDATE Books
                SET available_copies=available_copies+1
                WHERE book_id=?
            """, (book_id,))

        return "Book returned successfully."
    finally:
        conn.close()


def get_issue_records():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT
                Issue_Records.issue_id,
                Issue_Records.book_id,
                Books.title,
                Issue_Records.student_id,
                Students.name,
                Issue_Records.issue_date,
                Issue_Records.due_date,
                Issue_Records.return_date,
                Issue_Records.status
            FROM Issue_Records
            JOIN Books ON Issue_Records.book_id=Books.book_id
            JOIN Students ON Issue_Records.student_id=Students.student_id
            ORDER BY Issue_Records.issue_id DESC
        """).fetchall()
    finally:
        conn.close()


def get_active_issues():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT Books.title, Students.name,
                   Issue_Records.issue_date, Issue_Records.due_date
            FROM Issue_Records
            JOIN Books ON Issue_Records.book_id=Books.book_id
            JOIN Students ON Issue_Records.student_id=Students.student_id
            WHERE Issue_Records.status='ISSUED'
            ORDER BY Issue_Records.due_date
        """).fetchall()
    finally:
        conn.close()


# ================= SUMMARY / REPORT OPERATIONS =================

def get_dashboard_counts():
    conn = get_connection()
    try:
        total_books = conn.execute(
            "SELECT COUNT(*) FROM Books"
        ).fetchone()[0]
        total_students = conn.execute(
            "SELECT COUNT(*) FROM Students"
        ).fetchone()[0]
        issued_books = conn.execute(
            "SELECT COUNT(*) FROM Issue_Records WHERE status='ISSUED'"
        ).fetchone()[0]
        available_copies = conn.execute(
            "SELECT COALESCE(SUM(available_copies), 0) FROM Books"
        ).fetchone()[0]

        return {
            "total_books": total_books,
            "total_students": total_students,
            "issued_books": issued_books,
            "available_copies": available_copies
        }
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Library database initialized successfully!")
