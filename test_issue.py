
from database import (
    initialize_database,
    issue_book,
    return_book,
    get_issue_records,
    get_books
)

initialize_database()

print("========== ISSUE BOOK ==========")

try:
    print(issue_book("DEMO101", "STU101"))
except ValueError as e:
    print("Error:", e)

print("\n========== ISSUE HISTORY ==========")

for record in get_issue_records():
    print(record)

print("\n========== RETURN BOOK ==========")

try:
    print(return_book("DEMO101", "STU101"))
except ValueError as e:
    print("Error:", e)

print("\n========== UPDATED BOOK RECORD ==========")

for book in get_books("DEMO101"):
    print(book)

print("\n========== FINAL ISSUE HISTORY ==========")

for record in get_issue_records():
    print(record)
