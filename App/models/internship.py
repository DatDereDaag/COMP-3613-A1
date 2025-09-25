from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    title =  db.Column(db.String(50), nullable=False, unique=True)
    details = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='open')
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, employer_id, title, details, status):
        self.employer_id = employer_id
        self.title = title
        self.details = details
        self.status = status
        
    def to_json(self):
        return{
            'id': self.id,
            'employer_id': self.employer_id,
            'title': self.title,
            'details': self.details,
            'date_posted': self.date_posted
        }

