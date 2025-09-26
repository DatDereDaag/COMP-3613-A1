from App.models import Staff
from App.database import db

def get_all_staff():
    staff = Staff.query.all()
    return [staff_member.to_json() for staff_member in staff]

def create_new_staff(password):
    try:
        new_staff = Staff(password=password)
        db.session.add(new_staff)
        db.session.commit()
        print(f'Created staff member: {new_staff.to_json()}')
    except Exception as e:
        db.session.rollback()
        print(f'Error creating staff member: {e}')