from App.models import Employer
from App.database import db

def get_all_employers():
    employers = Employer.query.all()
    return [employer.to_json() for employer in employers]

def create_new_employer(company_name, password):
    try:
        new_employer = Employer(company_name=company_name, password=password)
        db.session.add(new_employer)
        db.session.commit()
        print(f'Created employer: {new_employer.to_json()}')
    except Exception as e:
        db.session.rollback()
        print(f'Error creating employer: {e}')