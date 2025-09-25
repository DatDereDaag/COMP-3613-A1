from werkzeug.security import check_password_hash, generate_password_hash
from .internship import *
from .shortlist import *
from .student import *
from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, password):
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def view_all_internships():
        return Internship.query.all().to_json()
    
    def view_all_students():
        return Student.query.all().to_json()
    
    def update_internship_shortlist(self, student_id, internship_id):
        shortlist_postion = Shortlist(student_id=student_id, internship_id=internship_id)
        db.session.add(shortlist_postion)
        db.session.commit()
        return shortlist_postion

