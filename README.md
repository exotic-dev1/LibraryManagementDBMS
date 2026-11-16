# Library Management System

A desktop-based Library Management System developed as a **Database
Management Systems (DBMS) project** using **Python**, **Tkinter**, and
**SQLite**.

The application helps manage book records, student records, book issue
and return operations, and borrowing history through a graphical user
interface.

## Features

-   **Dashboard:** Displays the number of book titles, total copies,
    registered students, and currently issued books.
-   **Book management:** Add, search, view, and delete book records.
-   **Student management:** Register, search, view, and delete student
    records.
-   **Book circulation:** Issue available books to registered students
    and process returns.
-   **Issue history:** View issue dates, due dates, return dates, and
    transaction status.
-   **Database integrity:** Uses primary keys, foreign keys, unique
    constraints, and check constraints.
-   **Transaction handling:** Issue and return operations update related
    records together.

> Note: The database module also includes book and student update
> functions. The current GUI focuses on the main add, search, delete,
> issue, return, and history workflows.

## Technologies Used

  Technology           Purpose
  -------------------- ---------------------------------------------
  Python 3             Application logic
  Tkinter              Desktop graphical user interface
  SQLite               Relational database
  SQL                  Database creation and CRUD/query operations
  Visual Studio Code   Development environment

SQLite and Tkinter are included with many standard Python installations.
No third-party Python packages are required for the current application.

## Project Structure

``` text
LibraryManagementDBMS/
├── main.py                 # Tkinter application
├── database.py             # SQLite connection, schema and database functions
├── test_database.py        # Tests book and student database operations
├── test_issue.py           # Tests book issue and return operations
├── library.db              # Local database (created automatically; do not commit)
├── docs/
│   ├── Library_Management_System_Report.pdf
│   └── Library_Management_System_Report.docx
├── screenshots/
│   ├── dashboard.png
│   ├── books.png
│   ├── students.png
│   ├── issue_confirmation.png
│   ├── issue_history.png
│   └── return_confirmation.png
├── .gitignore
└── README.md
```

The `docs/` and `screenshots/` folders are suggested locations. Add your
report and actual application screenshots using these filenames, or
update the paths below to match your repository.

## Requirements

-   Python 3.9 or later recommended
-   Windows, Linux, or macOS with Tkinter available
-   Git (optional, for cloning the repository)

Check your Python installation:

``` bash
python --version
```

If Tkinter is unavailable, install the Tkinter package provided for your
operating system.

## Installation and Setup

### 1. Clone the repository

``` bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Or download the repository as a ZIP file and extract it.

### 2. Open the project directory

``` bash
cd LibraryManagementDBMS
```

### 3. Run the application

``` bash
python main.py
```

The application initializes the SQLite database and creates the required
tables automatically on startup. The database file is named `library.db`
and is created in the working directory.

## Running the Tests

Test book and student database operations:

``` bash
python test_database.py
```

Test book issue and return operations:

``` bash
python test_issue.py
```

The test scripts use sample records such as:

-   Book ID: `DEMO101`
-   Student ID: `STU101`

Running the tests may add or modify sample data in the local database.

## Database Design

The database contains three main tables.

### 1. Students

  Attribute      Description
  -------------- ----------------------
  `student_id`   Primary key
  `name`         Student name
  `email`        Unique email address
  `phone`        Contact number

### 2. Books

  Attribute            Description
  -------------------- ----------------------------
  `book_id`            Primary key
  `title`              Book title
  `author`             Book author
  `genre`              Book category
  `total_copies`       Total number of copies
  `available_copies`   Copies currently available
  `location`           Shelf or storage location

### 3. Issue_Records

  Attribute       Description
  --------------- ------------------------------------------
  `issue_id`      Primary key
  `book_id`       Foreign key referencing `Books`
  `student_id`    Foreign key referencing `Students`
  `issue_date`    Date the book was issued
  `due_date`      Expected return date
  `return_date`   Actual return date; empty until returned
  `status`        `ISSUED` or `RETURNED`

**Relationships:**

-   One student can have multiple issue records.
-   One book can appear in multiple issue records over time.
-   Each issue record references one student and one book.

## Screenshots

Add your actual screenshots to the `screenshots/` directory and keep the
filenames below, or change the paths to match your files.

### Dashboard

![Library Management System dashboard](screenshots/dashboard.png)

### Book Management

![Book management screen](screenshots/books.png)

### Student Management

![Student management screen](screenshots/students.png)

### Issue Confirmation

![Book issue confirmation](screenshots/issue_confirmation.png)

### Issue History

![Book issue history](screenshots/issue_history.png)

### Return Confirmation

![Book return confirmation](screenshots/return_confirmation.png)

## Project Report

Place the project report in the `docs/` directory:

-   `Library_Management_System_Report.pdf`
-   `Library_Management_System_Report.docx`

## Concepts Demonstrated

-   Relational database design
-   Primary keys and foreign keys
-   UNIQUE, NOT NULL, and CHECK constraints
-   CRUD operations: Create, Read, Update, and Delete
-   SQL JOIN queries
-   Database transactions
-   Referential integrity and book availability

## Future Improvements

-   Login and role-based access for librarians and administrators
-   Overdue fine calculation and due-date reminders
-   Book reservation and renewal
-   Exportable reports
-   Support for multiple library branches

## Academic Project

**Project:** Library Management System\
**Subject:** Database Management Systems\
**Course:** B.Tech -- Computer Science and Applied Mathematics\
**Semester:** 5th\
**Academic Year:** 2026--27

------------------------------------------------------------------------

Developed as an academic project to demonstrate the practical
integration of Python with a relational database.
