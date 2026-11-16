
from database import (
    initialize_database,
    add_book,
    get_books,
    update_book,
    add_student,
    get_students,
    update_student
)

# Initialize database
initialize_database()

# Add sample book if it does not already exist
if not get_books("DEMO101"):
    print(add_book(
        "DEMO101",
        "Python Programming",
        "John Smith",
        "Programming",
        5,
        "Shelf A1"
    ))

# Add sample student if it does not already exist
if not get_students("STU101"):
    print(add_student(
        "STU101",
        "Rahul Sharma",
        "rahul@example.com",
        "9876543210"
    ))

# Display books
print("\n========== BOOK RECORDS ==========")
for book in get_books():
    print(book)

# Display students
print("\n========== STUDENT RECORDS ==========")
for student in get_students():
    print(student)

# Test update operations
print("\n========== UPDATE TEST ==========")

print(update_book(
    "DEMO101",
    "Python Programming",
    "John Smith",
    "Programming",
    "Shelf A2"
))

print(update_student(
    "STU101",
    "Rahul Sharma",
    "rahul@example.com",
    "9876543210"
))

print("\nAll CRUD tests completed!")
