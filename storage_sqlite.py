import os
import sqlite3
from typing import List, Optional
from student import Student


DB_FILE = "students.db"


def _get_connection():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade TEXT,
                email TEXT,
                phone TEXT
            )
            """
        )
        conn.commit()


def save_student(student: Student) -> None:
    _init_db()
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (id, name, age, grade, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
            (student.id, student.name, student.age, student.grade, student.email, student.phone),
        )
        conn.commit()


def load_students() -> List[Student]:
    _init_db()
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, grade, email, phone FROM students")
        rows = cur.fetchall()
        result: List[Student] = []
        for row in rows:
            s = Student(row[1], row[2], row[3], row[4], row[5])
            s.id = row[0]
            result.append(s)
        return result


def search_student(search_term: str, search_by: str = "name") -> List[Student]:
    _init_db()
    query_map = {
        "name": ("SELECT id, name, age, grade, email, phone FROM students WHERE LOWER(name) LIKE ?", f"%{search_term.lower()}%"),
        "id": ("SELECT id, name, age, grade, email, phone FROM students WHERE LOWER(id) LIKE ?", f"%{search_term.lower()}%"),
        "email": ("SELECT id, name, age, grade, email, phone FROM students WHERE LOWER(email) LIKE ?", f"%{search_term.lower()}%"),
    }
    sql, param = query_map.get(search_by, query_map["name"])
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, (param,))
        rows = cur.fetchall()
        results: List[Student] = []
        for row in rows:
            s = Student(row[1], row[2], row[3], row[4], row[5])
            s.id = row[0]
            results.append(s)
        return results


def update_student(student_id: str, **kwargs) -> bool:
    _init_db()
    allowed = {"name", "age", "grade", "email", "phone"}
    fields = []
    values = []
    for key, value in kwargs.items():
        if key in allowed:
            fields.append(f"{key} = ?")
            values.append(value)
    if not fields:
        return False
    values.append(student_id)
    sql = f"UPDATE students SET {', '.join(fields)} WHERE id = ?"
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, tuple(values))
        conn.commit()
        return cur.rowcount > 0


def delete_student(student_id: str) -> bool:
    _init_db()
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        return cur.rowcount > 0


def get_student_by_id(student_id: str) -> Optional[Student]:
    _init_db()
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, grade, email, phone FROM students WHERE id = ?", (student_id,))
        row = cur.fetchone()
        if not row:
            return None
        s = Student(row[1], row[2], row[3], row[4], row[5])
        s.id = row[0]
        return s


def import_from_pickle_if_needed():
    """If DB is empty and student.pkl exists, import students once."""
    _init_db()
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        count = cur.fetchone()[0]
        if count:
            return
    pkl_file = "student.pkl"
    if os.path.exists(pkl_file):
        import pickle
        try:
            with open(pkl_file, "rb") as f:
                students = pickle.load(f)
            for s in students:
                save_student(s)
        except Exception:
            # Ignore import failures; keep DB empty
            pass


# Ensure DB exists on import and import old data once
_init_db()
import_from_pickle_if_needed()

