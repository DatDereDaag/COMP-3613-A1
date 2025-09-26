from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy import UniqueConstraint

class Shortlist(db.Model):
    __tablename__ = 'shortlist'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'))
    status = db.Column(db.String(100), default="pending")
    date_added = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('student_id', 'internship_id', name='uq_student_internship'),
    )

    def __init__(self, student_id, internship_id):
        self.student_id = student_id
        self.internship_id = internship_id

    def to_json(self):
        return{
            'id': self.id,
            'student_id' : self.student_id,
            'internship_id' : self.internship_id,
            'status' : self.status,
            'date_added' : self.date_added.strftime("%Y-%m-%d %H:%M:%S")
        }
