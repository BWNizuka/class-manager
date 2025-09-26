from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, person_id: str, name: str, email: str):
        self.person_id = person_id
        self.name = name
        self.email = email

    @abstractmethod
    def to_dict(self):
        pass

class Student(Person):
    def __init__(self, person_id, name, email, grade_level):
        super().__init__(person_id, name, email)
        self.grade_level = grade_level
        self.enrollments = []

    def to_dict(self):
        return {
            "student_id": self.person_id,
            "name": self.name,
            "email": self.email,
            "grade_level": self.grade_level,
            "enrollments": self.enrollments
        }

class Teacher(Person):
    def __init__(self, person_id, name, email, specialization):
        super().__init__(person_id, name, email)
        self.specialization = specialization
        self.courses = []

    def to_dict(self):
        return {
            "teacher_id": self.person_id,
            "name": self.name,
            "email": self.email,
            "specialization": self.specialization,
            "courses": self.courses
        }

class Course:
    def __init__(self, code, title, schedule):
        self.code = code
        self.title = title
        self.schedule = schedule
        self.teacher_id = None
        self.students = []

    def to_dict(self):
        return {
            "course_code": self.code,
            "title": self.title,
            "schedule": self.schedule,
            "teacher_id": self.teacher_id,
            "students": self.students
        }
