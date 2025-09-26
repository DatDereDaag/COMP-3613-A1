from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .internship import *
from .shortlist import *

class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    internships = db.relationship('Internship', backref='employer', lazy=True, cascade="all, delete-orphan")

    def __init__(self, company_name, password):
        self.company_name = company_name
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def create_internship(self, title, details):
        new_internship = Internship(title=title, details=details, employer_id=self.id)
        db.session.add(new_internship)
        db.session.commit()
        return new_internship
    
    def get_posted_internships(self):
        return Internship.query.filter_by(employer_id=self.id).all()
    
    def delete_internship(self, internship_id):
        internship = Internship.query.filter_by(id=internship_id, employer_id=self.id).first()
        if internship:
            db.session.delete(internship)
            db.session.commit()
            return True
        return False
    
    def update_internship(self, internship_id, title=None, details=None, status=None):
        internship = Internship.query.filter_by(id=internship_id, employer_id=self.id).first()
        if internship:
            if title:
                internship.title = title
            if details:
                internship.details = details
            if status:
                internship.status = status    

            db.session.commit()
            return internship
        return None
    
    def get_internship_shortlist(self, internship_id):
        return Shortlist.query.filter_by(internship_id=internship_id).all()

    def update_internship_shortlist_status(self, shortlist_id, status):
        shortlist = Shortlist.query.filter_by(id=shortlist_id).first()
        if shortlist:
            shortlist.status = status
            db.session.commit()
            return shortlist
        return None
    
    def to_json(self):
        return{
            'id': self.id,
            'company_name': self.company_name
        }
