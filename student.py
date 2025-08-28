import uuid

class Student:
    def __init__(self, name, age, grade=None, email=None, phone=None):
        self.id = str(uuid.uuid4())[:8]  # Generate unique 8-character ID
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email
        self.phone = phone
    
    def display(self):
        return f"ID: {self.id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}, Email: {self.email}, Phone: {self.phone}"
    
    def __str__(self):
        return self.display()
    
    def to_dict(self):
        """Convert student object to dictionary for easier handling"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'email': self.email,
            'phone': self.phone
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create student object from dictionary"""
        student = cls(data['name'], data['age'], data.get('grade'), data.get('email'), data.get('phone'))
        student.id = data['id']
        return student