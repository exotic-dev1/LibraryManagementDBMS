import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    initialize_database,
    add_book, get_books, delete_book,
    add_student, get_students, delete_student,
    issue_book, return_book, get_issue_records
)


class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f3f5f7")

        initialize_database()
        self.setup_style()
        self.build_header()
        self.build_dashboard()
        self.build_tabs()
        self.refresh_all()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TNotebook", background="#f3f5f7", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("TButton", padding=7, font=("Segoe UI", 9))
        style.configure("Header.TLabel", background="#172b4d", foreground="white",
                        font=("Segoe UI", 19, "bold"))
        style.configure("SubHeader.TLabel", background="#172b4d", foreground="#dce6f2",
                        font=("Segoe UI", 9))

    def build_header(self):
        header = tk.Frame(self.root, bg="#172b4d", height=82)
        header.pack(fill="x")
        header.pack_propagate(False)
        ttk.Label(header, text="LIBRARY MANAGEMENT SYSTEM",
                  style="Header.TLabel").pack(anchor="w", padx=24, pady=(14, 0))
        ttk.Label(header, text="Book records • Student records • Issue and return tracking",
                  style="SubHeader.TLabel").pack(anchor="w", padx=26)

    def build_dashboard(self):
        self.dashboard = tk.Frame(self.root, bg="#f3f5f7")
        self.dashboard.pack(fill="x", padx=18, pady=14)
        self.stat_labels = {}
        for key, title in [
            ("books", "BOOK TITLES"),
            ("copies", "TOTAL COPIES"),
            ("students", "REGISTERED STUDENTS"),
            ("issued", "CURRENTLY ISSUED"),
        ]:
            card = tk.Frame(self.dashboard, bg="white", bd=1, relief="solid")
            card.pack(side="left", fill="x", expand=True, padx=5)
            tk.Label(card, text=title, bg="white", fg="#64748b",
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
            value = tk.Label(card, text="0", bg="white", fg="#172b4d",
                             font=("Segoe UI", 20, "bold"))
            value.pack(anchor="w", padx=14, pady=(0, 10))
            self.stat_labels[key] = value

    def build_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.books_tab = ttk.Frame(self.tabs, padding=12)
        self.students_tab = ttk.Frame(self.tabs, padding=12)
        self.circulation_tab = ttk.Frame(self.tabs, padding=12)
        self.history_tab = ttk.Frame(self.tabs, padding=12)

        self.tabs.add(self.books_tab, text="Books")
        self.tabs.add(self.students_tab, text="Students")
        self.tabs.add(self.circulation_tab, text="Issue / Return")
        self.tabs.add(self.history_tab, text="Issue History")

        self.build_books_tab()
        self.build_students_tab()
        self.build_circulation_tab()
        self.build_history_tab()

    def make_tree(self, parent, columns, headings, widths=None):
        wrap = ttk.Frame(parent)
        wrap.pack(fill="both", expand=True, pady=8)
        tree = ttk.Treeview(wrap, columns=columns, show="headings")
        ybar = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        xbar = ttk.Scrollbar(wrap, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        ybar.grid(row=0, column=1, sticky="ns")
        xbar.grid(row=1, column=0, sticky="ew")
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        for i, (col, heading) in enumerate(zip(columns, headings)):
            tree.heading(col, text=heading)
            tree.column(col, width=(widths[i] if widths else 120), anchor="center")
        return tree

    def build_books_tab(self):
        form = ttk.LabelFrame(self.books_tab, text="Add New Book", padding=10)
        form.pack(fill="x")
        self.book_vars = {k: tk.StringVar() for k in
                          ("id", "title", "author", "genre", "copies", "location")}
        fields = [
            ("Book ID", "id"), ("Title", "title"), ("Author", "author"),
            ("Genre", "genre"), ("Total Copies", "copies"), ("Shelf / Location", "location")
        ]
        for i, (label, key) in enumerate(fields):
            r, c = divmod(i, 3)
            ttk.Label(form, text=label).grid(row=r*2, column=c, sticky="w", padx=6, pady=(2, 0))
            ttk.Entry(form, textvariable=self.book_vars[key], width=30).grid(
                row=r*2+1, column=c, sticky="ew", padx=6, pady=(0, 6))
            form.columnconfigure(c, weight=1)

        actions = ttk.Frame(self.books_tab)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Add Book", command=self.add_book_action).pack(side="left", padx=3)
        ttk.Button(actions, text="Delete Selected Book", command=self.delete_book_action).pack(side="left", padx=3)
        ttk.Button(actions, text="Refresh", command=self.refresh_books).pack(side="left", padx=3)
        self.book_search = tk.StringVar()
        ttk.Label(actions, text="Search:").pack(side="left", padx=(20, 5))
        search = ttk.Entry(actions, textvariable=self.book_search, width=24)
        search.pack(side="left")
        search.bind("<KeyRelease>", lambda event: self.refresh_books())

        self.book_tree = self.make_tree(
            self.books_tab,
            ("id", "title", "author", "genre", "total", "available", "location"),
            ("BOOK ID", "TITLE", "AUTHOR", "GENRE", "TOTAL", "AVAILABLE", "LOCATION"),
            (100, 190, 150, 120, 75, 85, 110)
        )

    def build_students_tab(self):
        form = ttk.LabelFrame(self.students_tab, text="Register Student", padding=10)
        form.pack(fill="x")
        self.student_vars = {k: tk.StringVar() for k in ("id", "name", "email", "phone")}
        fields = [("Student ID", "id"), ("Full Name", "name"),
                  ("Email", "email"), ("Phone", "phone")]
        for i, (label, key) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=i, sticky="w", padx=6)
            ttk.Entry(form, textvariable=self.student_vars[key], width=25).grid(
                row=1, column=i, sticky="ew", padx=6, pady=4)
            form.columnconfigure(i, weight=1)

        actions = ttk.Frame(self.students_tab)
        actions.pack(fill="x", pady=8)
        ttk.Button(actions, text="Register Student", command=self.add_student_action).pack(side="left", padx=3)
        ttk.Button(actions, text="Delete Selected Student", command=self.delete_student_action).pack(side="left", padx=3)
        ttk.Button(actions, text="Refresh", command=self.refresh_students).pack(side="left", padx=3)
        self.student_search = tk.StringVar()
        ttk.Label(actions, text="Search:").pack(side="left", padx=(20, 5))
        search = ttk.Entry(actions, textvariable=self.student_search, width=24)
        search.pack(side="left")
        search.bind("<KeyRelease>", lambda event: self.refresh_students())

        self.student_tree = self.make_tree(
            self.students_tab, ("id", "name", "email", "phone"),
            ("STUDENT ID", "NAME", "EMAIL", "PHONE"), (130, 220, 250, 140)
        )

    def build_circulation_tab(self):
        form = ttk.LabelFrame(self.circulation_tab, text="Book Circulation", padding=18)
        form.pack(fill="x", pady=8)
        self.circulation_book = tk.StringVar()
        self.circulation_student = tk.StringVar()

        ttk.Label(form, text="Book ID").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(form, textvariable=self.circulation_book, width=30).grid(
            row=0, column=1, padx=8, pady=6)
        ttk.Label(form, text="Student ID").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(form, textvariable=self.circulation_student, width=30).grid(
            row=1, column=1, padx=8, pady=6)

        buttons = ttk.Frame(form)
        buttons.grid(row=2, column=0, columnspan=2, pady=12)
        ttk.Button(buttons, text="Issue Book", command=self.issue_book_action).pack(side="left", padx=8)
        ttk.Button(buttons, text="Return Book", command=self.return_book_action).pack(side="left", padx=8)
        ttk.Button(buttons, text="Clear", command=self.clear_circulation).pack(side="left", padx=8)

        ttk.Label(self.circulation_tab,
                  text="The standard loan period is 7 days. Issue and return activity is saved in Issue History.",
                  foreground="#475569").pack(anchor="w", pady=8)

    def build_history_tab(self):
        bar = ttk.Frame(self.history_tab)
        bar.pack(fill="x")
        ttk.Button(bar, text="Refresh History", command=self.refresh_history).pack(side="left")
        self.history_tree = self.make_tree(
            self.history_tab,
            ("issue_id", "book_id", "title", "student_id", "student",
             "issue_date", "due_date", "return_date", "status"),
            ("ISSUE ID", "BOOK ID", "BOOK TITLE", "STUDENT ID", "STUDENT NAME",
             "ISSUE DATE", "DUE DATE", "RETURN DATE", "STATUS"),
            (75, 90, 150, 95, 145, 100, 100, 100, 90)
        )

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def refresh_books(self):
        self.clear_tree(self.book_tree)
        for row in get_books(self.book_search.get().strip()):
            self.book_tree.insert("", "end", values=row)

    def refresh_students(self):
        self.clear_tree(self.student_tree)
        for row in get_students(self.student_search.get().strip()):
            self.student_tree.insert("", "end", values=row)

    def refresh_history(self):
        self.clear_tree(self.history_tree)
        for row in get_issue_records():
            self.history_tree.insert("", "end", values=row)

    def refresh_dashboard(self):
        books = get_books()
        students = get_students()
        history = get_issue_records()
        total_copies = sum(int(row[4]) for row in books)
        currently_issued = sum(1 for row in history if row[-1] == "ISSUED")
        self.stat_labels["books"].config(text=str(len(books)))
        self.stat_labels["copies"].config(text=str(total_copies))
        self.stat_labels["students"].config(text=str(len(students)))
        self.stat_labels["issued"].config(text=str(currently_issued))

    def refresh_all(self):
        self.refresh_books()
        self.refresh_students()
        self.refresh_history()
        self.refresh_dashboard()

    def add_book_action(self):
        v = self.book_vars
        try:
            copies = int(v["copies"].get())
            if copies < 0:
                raise ValueError("Total copies cannot be negative.")
            if not all(v[k].get().strip() for k in ("id", "title", "author", "genre", "location")):
                raise ValueError("Please fill in all book fields.")
            messagebox.showinfo("Success", add_book(
                v["id"].get().strip(), v["title"].get().strip(),
                v["author"].get().strip(), v["genre"].get().strip(),
                copies, v["location"].get().strip()
            ))
            for item in v.values():
                item.set("")
            self.refresh_all()
        except (ValueError, TypeError) as e:
            messagebox.showerror("Unable to add book", str(e))

    def delete_book_action(self):
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Select book", "Please select a book first.")
            return
        book_id = self.book_tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete book {book_id}?"):
            return
        try:
            messagebox.showinfo("Success", delete_book(book_id))
            self.refresh_all()
        except ValueError as e:
            messagebox.showerror("Unable to delete", str(e))

    def add_student_action(self):
        v = self.student_vars
        if not all(v[k].get().strip() for k in ("id", "name", "phone")):
            messagebox.showerror("Missing details", "Student ID, name and phone are required.")
            return
        try:
            messagebox.showinfo("Success", add_student(
                v["id"].get().strip(), v["name"].get().strip(),
                v["email"].get().strip(), v["phone"].get().strip()
            ))
            for item in v.values():
                item.set("")
            self.refresh_all()
        except ValueError as e:
            messagebox.showerror("Unable to register student", str(e))

    def delete_student_action(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Select student", "Please select a student first.")
            return
        student_id = self.student_tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete student {student_id}?"):
            return
        try:
            messagebox.showinfo("Success", delete_student(student_id))
            self.refresh_all()
        except ValueError as e:
            messagebox.showerror("Unable to delete", str(e))

    def issue_book_action(self):
        book_id = self.circulation_book.get().strip()
        student_id = self.circulation_student.get().strip()
        if not book_id or not student_id:
            messagebox.showwarning("Missing details", "Enter both Book ID and Student ID.")
            return
        try:
            messagebox.showinfo("Issue Book", issue_book(book_id, student_id))
            self.refresh_all()
        except ValueError as e:
            messagebox.showerror("Unable to issue book", str(e))

    def return_book_action(self):
        book_id = self.circulation_book.get().strip()
        student_id = self.circulation_student.get().strip()
        if not book_id or not student_id:
            messagebox.showwarning("Missing details", "Enter both Book ID and Student ID.")
            return
        try:
            messagebox.showinfo("Return Book", return_book(book_id, student_id))
            self.refresh_all()
        except ValueError as e:
            messagebox.showerror("Unable to return book", str(e))

    def clear_circulation(self):
        self.circulation_book.set("")
        self.circulation_student.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
