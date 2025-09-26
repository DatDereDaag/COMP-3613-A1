from App.models import Student
from App.database import db

def get_all_students():
    students = Student.query.all()
    return [student.to_json() for student in students]

def create_new_student(degree, courses, gpa, password):
    try:
        new_student = Student(degree=degree, courses=courses, gpa=gpa, password=password)
        db.session.add(new_student)
        db.session.commit()
        print(f'Created student: {new_student.to_json()}')
    except Exception as e:
        db.session.rollback()
        print(f'Error creating student: {e}')