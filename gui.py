import tkinter as tk
from tkinter import ttk, messagebox
from student import Student
from storage_sqlite import load_students, save_student, search_student, update_student, delete_student


class StudentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")

        self._build_widgets()
        self._populate_table()

    def _build_widgets(self):
        form = ttk.Frame(self.root, padding=10)
        form.grid(row=0, column=0, sticky="ew")

        # Labels and entries
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.grade_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.name_var, width=24).grid(row=0, column=1, padx=5)
        ttk.Label(form, text="Age").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.age_var, width=8).grid(row=0, column=3, padx=5)
        ttk.Label(form, text="Grade").grid(row=0, column=4, sticky="w")
        ttk.Entry(form, textvariable=self.grade_var, width=10).grid(row=0, column=5, padx=5)

        ttk.Label(form, text="Email").grid(row=1, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.email_var, width=24).grid(row=1, column=1, padx=5)
        ttk.Label(form, text="Phone").grid(row=1, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.phone_var, width=16).grid(row=1, column=3, padx=5)

        ttk.Button(form, text="Add", command=self._on_add_update).grid(row=1, column=5, sticky="e")

        # Search bar
        search_bar = ttk.Frame(self.root, padding=(10, 0))
        search_bar.grid(row=1, column=0, sticky="ew")
        self.search_var = tk.StringVar()
        self.search_by_var = tk.StringVar(value="name")
        ttk.Entry(search_bar, textvariable=self.search_var, width=30).grid(row=0, column=0, padx=(0, 6))
        ttk.Combobox(search_bar, textvariable=self.search_by_var, values=["name", "id", "email"], width=10, state="readonly").grid(row=0, column=1)
        ttk.Button(search_bar, text="Search", command=self._on_search).grid(row=0, column=2, padx=6)
        ttk.Button(search_bar, text="Reset", command=self._populate_table).grid(row=0, column=3)

        # Table
        table_frame = ttk.Frame(self.root, padding=10)
        table_frame.grid(row=2, column=0, sticky="nsew")
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        columns = ("id", "name", "age", "grade", "email", "phone")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        # Row actions
        actions = ttk.Frame(self.root, padding=(10, 10))
        actions.grid(row=3, column=0, sticky="ew")
        ttk.Button(actions, text="Delete Selected", command=self._on_delete).grid(row=0, column=0)
        ttk.Button(actions, text="Load to Form", command=self._on_load_to_form).grid(row=0, column=1, padx=8)

    def _populate_table(self, students=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if students is None:
            students = load_students()
        for s in students:
            self.tree.insert("", "end", values=(s.id, s.name, s.age, s.grade, s.email, s.phone))

    def _on_add_update(self):
        name = self.name_var.get().strip()
        age_text = self.age_var.get().strip()
        if not name or not age_text.isdigit():
            messagebox.showerror("Invalid input", "Name and numeric Age are required.")
            return
        age = int(age_text)
        grade = self.grade_var.get().strip() or None
        email = self.email_var.get().strip() or None
        phone = self.phone_var.get().strip() or None

        # If an ID is selected, update; otherwise add
        selected = self.tree.selection()
        if selected:
            sid = self.tree.item(selected[0], 'values')[0]
            ok = update_student(sid, name=name, age=age, grade=grade, email=email, phone=phone)
            if ok:
                messagebox.showinfo("Success", "Student updated")
            else:
                messagebox.showerror("Error", "Update failed")
        else:
            stu = Student(name, age, grade, email, phone)
            save_student(stu)
            messagebox.showinfo("Success", "Student added")
        self._populate_table()
        self._clear_form()

    def _on_search(self):
        term = self.search_var.get().strip()
        by = self.search_by_var.get()
        if not term:
            self._populate_table()
            return
        results = search_student(term, by)
        self._populate_table(results)

    def _on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Please select a row to delete")
            return
        sid = self.tree.item(selected[0], 'values')[0]
        if messagebox.askyesno("Confirm", "Delete selected student?"):
            delete_student(sid)
            self._populate_table()
            self._clear_form()

    def _on_load_to_form(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Please select a row to load")
            return
        values = self.tree.item(selected[0], 'values')
        _, name, age, grade, email, phone = values
        self.name_var.set(name)
        self.age_var.set(age)
        self.grade_var.set(grade)
        self.email_var.set(email)
        self.phone_var.set(phone)

    def _clear_form(self):
        self.name_var.set("")
        self.age_var.set("")
        self.grade_var.set("")
        self.email_var.set("")
        self.phone_var.set("")


def launch():
    root = tk.Tk()
    StudentGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch()

