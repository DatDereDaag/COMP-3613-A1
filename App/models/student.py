from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .shortlist import *

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    courses = db.Column(db.String(2560), nullable=True)
    gpa = db.Column(db.Float, nullable=True)

    shortlisted_positions = db.relationship('Internship', secondary = 'shortlist', backref='shortlist', lazy='dynamic')

    def __init__(self, degree, courses, gpa, password):
        self.degree = degree
        self.courses = courses
        self.gpa = gpa
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def view_shortlisted_positions(self):
        return Shortlist.query.filter_by(student_id = self.student_id).all().to_json()
    
    def to_json(self):
        return{
            'id': self.id,
            'degree': self.degree,
            'courses': self.courses,
            'gpa': self.gpa
        }
    