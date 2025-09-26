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

    def get_all_internships():
        return Internship.query.all()
    
    def get_all_students():
        return Student.query.all()
    
    def create_internship_shortlist_position(self, student_id, internship_id):
        shortlist_postion = Shortlist(student_id=student_id, internship_id=internship_id)
        db.session.add(shortlist_postion)
        try:
            db.session.commit()
            return shortlist_postion
        except Exception as e:
            db.session.rollback()
            print("Error: Student already shortlisted for this position")
            return None

    def to_json(self):
        return{
            'id': self.id
        }
