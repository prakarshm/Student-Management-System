from student import Student
import os
import pickle

# Use relative path for better portability
file = "student.pkl"

def save_student(s):
    students = []
    if os.path.exists(file):
        with open(file, "rb") as f:
            students = pickle.load(f)
    students.append(s)
    with open(file, "wb") as f:
        pickle.dump(students, f)

def load_students():
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    return []

def get_students_display():
    """Get list of students as display strings"""
    students = load_students()
    return [student.display() for student in students]

def search_student(search_term, search_by="name"):
    """Search for students by name, id, or email"""
    students = load_students()
    results = []
    
    for student in students:
        if search_by == "name" and search_term.lower() in student.name.lower():
            results.append(student)
        elif search_by == "id" and search_term.lower() in student.id.lower():
            results.append(student)
        elif search_by == "email" and student.email and search_term.lower() in student.email.lower():
            results.append(student)
    
    return results



def delete_student(student_id):
    """Delete a student by ID"""
    students = load_students()
    students = [s for s in students if s.id != student_id]
    with open(file, "wb") as f:
        pickle.dump(students, f)
    return True

def get_student_by_id(student_id):
    """Get a specific student by ID"""
    students = load_students()
    for student in students:
        if student.id == student_id:
            return student
    return None

# Initialize with some sample data if file doesn't exist
if not os.path.exists(file):
    s1 = Student("Alice Johnson", 20, "A", "alice@email.com", "123-456-7890")
    s2 = Student("Bob Smith", 22, "B+", "bob@email.com", "987-654-3210")
    s3 = Student("Carol Davis", 19, "A-", "carol@email.com", "555-123-4567")
    save_student(s1)
    save_student(s2)
    save_student(s3)
