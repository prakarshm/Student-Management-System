from student import Student
import os  
import pickle
# Switch to SQLite-backed storage while keeping the same API
from storage_sqlite import (
    save_student,
    load_students,
    search_student,
    update_student,
    delete_student,
)


def prompt_student_details(existing=None):
    name = input(f"Enter student's name{f" [{existing.name}]" if existing else ''}: ") or (existing.name if existing else '')
    age_input = input(f"Enter student's age{f" [{existing.age}]" if existing else ''}: ")
    age = int(age_input) if age_input else (existing.age if existing else 0)
    grade = input(f"Enter grade{f" [{existing.grade}]" if existing else ''}: ") or (existing.grade if existing else None)
    email = input(f"Enter email{f" [{existing.email}]" if existing else ''}: ") or (existing.email if existing else None)
    phone = input(f"Enter phone{f" [{existing.phone}]" if existing else ''}: ") or (existing.phone if existing else None)
    return name, age, grade, email, phone


def menu():
    while True:
        choice = input(
            """Student Management System
                    1. Add Student
                    2. View Students
                    3. Search Student
                    4. Update Student
                    5. Delete Student
                    6. Launch GUI
                    0. Exit
                    Enter your choice: """
        )
        if choice == '1':
            name, age, grade, email, phone = prompt_student_details()
            s1 = Student(name, age, grade, email, phone)
            save_student(s1)
            print("Student added.")
        elif choice == '2':
            students = load_students()
            if students:
                for student in students:
                    print(student)
            else:
                print("No students found.")
        elif choice == '3':
            term = input("Search term: ")
            by = input("Search by (name/id/email) [name]: ") or 'name'
            results = search_student(term, by)
            if results:
                for s in results:
                    print(s)
            else:
                print("No matches.")
        elif choice == '4':
            sid = input("Enter Student ID to update: ")
            # Find exact student for defaults
            matches = search_student(sid, 'id')
            existing = matches[0] if matches else None
            if not existing:
                print("Student not found.")
                continue
            name, age, grade, email, phone = prompt_student_details(existing)
            updated = update_student(
                existing.id,
                name=name,
                age=age,
                grade=grade,
                email=email,
                phone=phone,
            )
            print("Updated." if updated else "Update failed.")
        elif choice == '5':
            sid = input("Enter Student ID to delete: ")
            ok = delete_student(sid)
            print("Deleted." if ok else "Delete failed.")
        elif choice == '6':
            try:
                import gui  # noqa: F401
                gui.launch()
            except Exception as e:
                print(f"Failed to launch GUI: {e}")
        elif choice == '0':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()