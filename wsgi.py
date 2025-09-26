import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.models import *
from App.controllers import *
from App.main import create_app


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    db.drop_all()
    db.create_all()

    employer1 = Employer(company_name='Test Company', password='testpass')
    staff1 = Staff(password='staffpass')
    student1 = Student(degree='Computer Science', courses='COMP2601, COMP3602', gpa=3.5, password='studentpass')

    db.session.add_all([employer1, staff1, student1])
    db.session.commit()
    print('database intialized')

@app.cli.command("list-employers", help="List all employers")
def list_employers():
    print(get_all_employers())

@app.cli.command("list-staff", help="List all staff")
def list_staff():
    print(get_all_staff())

@app.cli.command("list-students", help="List all students")
def list_students():
    print(get_all_students())

@app.cli.command("create-employer", help="Create a new employer")
@click.argument("company_name")
@click.argument("password")
def create_employer(company_name, password):
    create_new_employer(company_name, password)

@app.cli.command("create-staff", help="Create a new staff member")
@click.argument("password")
def create_staff(password):
    create_new_staff(password)

@app.cli.command("create-student", help="Create a new student")
@click.argument("degree")
@click.argument("courses")
@click.argument("gpa", type=float)
@click.argument("password")
def create_student(degree, courses, gpa, password):
    create_new_student(degree, courses, gpa, password)

'''
Employer Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
employer_cli = AppGroup('employer', help='Employer object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@employer_cli.command("create-internship", help="Creates an internship")
@click.argument("title")
@click.argument("details")
@click.argument("employer_id", type=int)
def create_internship_command(title, details, employer_id):
    employer = Employer.query.get(employer_id)
    if employer:
        internship = employer.create_internship(title=title, details=details)
        print(f'Created internship: {internship.to_json()}')
    else:
        print(f'Employer with id {employer_id} not found.')

@employer_cli.command("view-internships", help="View employer's posted internships")
@click.argument("employer_id", type=int)
def view_internships_command(employer_id):
    employer = Employer.query.get(employer_id)
    if employer:
        internships = employer.get_posted_internships()
        print(f'Employer {employer.company_name} posted internships:')

        if not internships or len(internships) == 0:
            print(f'No internships found for employer {employer.company_name}.')
            return

        for internship in internships:
            print(internship.to_json())
    else:
        print(f'Employer with id {employer_id} not found.')

@employer_cli.command("delete-internship", help="Delete an internship")
@click.argument("employer_id", type=int)
def delete_internship_command(employer_id):
    employer = Employer.query.get(employer_id)
    if employer:
        internships = employer.get_posted_internships()
        print(f'Internships posted by {employer.company_name}:')

        if not internships or len(internships) == 0:
            print(f'No internships found for employer {employer.company_name}.')
            return

        for internship in internships:
            print(internship.to_json())
        internship_id = click.prompt("Enter the ID of the internship to delete", type=int)
        selected_internship = employer.delete_internship(internship_id)
        if selected_internship:
            print(f'Internship with id {internship_id} deleted successfully.')
        else:
            print(f'Internship with id {internship_id} not found or could not be deleted.')
    else:
        print(f'Employer with id {employer_id} not found.')

@employer_cli.command("update-internship", help="Update an internship")
@click.argument("employer_id", type=int)
def update_internship_command(employer_id):
    employer = Employer.query.get(employer_id)
    if employer:
        internships = employer.get_posted_internships()
        print(f'Internships posted by {employer.company_name}:')

        if not internships or len(internships) == 0:
            print(f'No internships found for employer {employer.company_name}.')
            return

        for internship in internships:
            print(internship.to_json())
        
        internship_id = click.prompt("Enter the ID of the internship to update", type=int)
        title = click.prompt("Enter new title (leave blank to keep current)", default="", show_default=False)
        details = click.prompt("Enter new details (leave blank to keep current)", default="", show_default=False)
        status = click.prompt("Enter new status (leave blank to keep current)", default="", show_default=False)
        
        updated_internship = employer.update_internship(internship_id, title, details, status)

        if updated_internship:
            print(f'Internship updated successfully: {updated_internship.to_json()}')
        else:
            print(f'Internship with id {internship_id} not found or could not be updated.')
    else:
        print(f'Employer with id {employer_id} not found.')

@employer_cli.command("view-internship-shortlist", help="View internship shortlist")
@click.argument("employer_id", type=int)
@click.argument("internship_id", type=int)
def view_internship_shortlist_command(employer_id, internship_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        print(f'Employer with id {employer_id} not found.')
        return
    
    internship = Internship.query.get(internship_id)
    if not internship or internship.employer_id != employer_id:
        print(f'Internship with id {internship_id} not found for employer {employer.company_name}.')
        return
    
    shortlist = employer.get_internship_shortlist(internship_id)
    print(f'Shortlist for internship {internship.title} posted by {employer.company_name}:')

    if shortlist is None or len(shortlist) == 0:
        print('No shortlist entries found.')
        return
    
    for entry in shortlist:
        print(entry.to_json())

@employer_cli.command("update-shortlist-status", help="Update shortlist status")
@click.argument("employer_id", type=int)
@click.argument("internship_id", type=int)
def update_shortlist_status_command(employer_id, internship_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        print(f'Employer with id {employer_id} not found.')
        return
     
    internship = Internship.query.get(internship_id)
    if not internship or internship.employer_id != employer_id:
        print(f'Internship with id {internship_id} not found for employer {employer.company_name}.')
        return
    
    shortlist = employer.get_internship_shortlist(internship_id)
    print(f'Shortlist for internship {internship.title}:')

    if shortlist is None or len(shortlist) == 0:
        print('No shortlist entries found.')
        return

    for entry in shortlist:
        print(entry.to_json())

    shortlist_id = click.prompt("Enter the ID of the shortlist entry to update status", type=int)
    new_status = click.prompt("Enter new status", type=str)
    updated_entry = employer.update_internship_shortlist_status(shortlist_id, new_status)
    if updated_entry:
        print(f'Shortlist entry updated successfully: {updated_entry.to_json()}')
    else:
        print(f'Shortlist entry with id {shortlist_id} not found or could not be updated.')
    

app.cli.add_command(employer_cli) # add the group to the cli

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("view-all-internships", help="View all internships")
def view_all_internships_command():
    internships = Staff.get_all_internships()
    if not internships or len(internships) == 0:
        print('No internships found.')
        return
    for internship in internships:
        print(internship.to_json())

@staff_cli.command("view-all-students", help="View all students")
def view_all_students_command():
    students = Staff.get_all_students()
    if not students or len(students) == 0:
        print('No students found.')
        return
    for student in students:
        print(student.to_json())

@staff_cli.command("create-shortlist-position", help="Create internship shortlist position")
@click.argument("staff_id", type=int)
@click.argument("student_id", type=int)
def create_shortlist_position_command(staff_id, student_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        print(f'Staff with id {staff_id} not found.')
        return
    
    student = Student.query.get(student_id)
    if not student:
        print(f'Student with id {student_id} not found.')
        return

    internships = Staff.get_all_internships()
    if not internships or len(internships) == 0:
        print('No internships found.')
        return

    print('Available internships:')
    for internship in internships:
        print(internship.to_json())
    
    internship_id = click.prompt("Enter the ID of the internship to shortlist the student for", type=int)
    selected_internship = Internship.query.get(internship_id)
    if not selected_internship:
        print(f'Internship with id {internship_id} not found.')
        return

    shortlist_position = staff.create_internship_shortlist_position(student_id, internship_id)

    if not shortlist_position:
        print(f'Could not create shortlist position')
        return
    print(f'Created shortlist position: {shortlist_position.to_json()}')


app.cli.add_command(staff_cli)


'''
Student Commands
'''
student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("view-shortlisted-positions", help="View student's shortlisted positions")
@click.argument("student_id", type=int)
def view_shortlisted_positions_command(student_id):
    student = Student.query.get(student_id)
    if not student:
        print(f'Student with id {student_id} not found.')
        return
    
    shortlist = student.get_shortlisted_positions()
    print(f'Shortlisted positions for student {student_id}:')

    if not shortlist or len(shortlist) == 0:
        print('No shortlisted positions found.')
        return

    for entry in shortlist:
        print(entry.to_json())

app.cli.add_command(student_cli)