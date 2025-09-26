# Internship Management System CLI

This project provides a command-line interface (CLI) built with Flask and Click for managing an internship system, including operations for **Employers**, **Staff**, and **Students**.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need **Python 3** and **Flask** installed. The project also relies on `click`, `pytest`, and specific Flask extensions like `Flask-Migrate`.

### Installation

1.  **Clone the repository** (assuming this code is part of a larger Flask application):
    ```bash
    git clone https://github.com/DatDereDaag/COMP-3613-A1
    cd [your-project-directory]
    ```
2.  **Set up a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies** (assuming a `requirements.txt` exists that includes Flask, Click, etc.):
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ CLI Commands

All commands are executed using the `flask` command, followed by the command name or group and command name.

### General Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `flask init` | **Creates and initializes the database**, dropping all existing data and creating sample `Employer`, `Staff`, and `Student` records. | `flask init` |
| `flask list-employers` | List all existing employers in the database. | `flask list-employers` |
| `flask list-staff` | List all existing staff members. | `flask list-staff` |
| `flask list-students` | List all existing students. | `flask list-students` |
| `flask create-employer <company_name> <password>` | Create a new employer record. | `flask create-employer "Tech Corp" "securepass123"` |
| `flask create-staff <password>` | Create a new staff member record. | `flask create-staff "staffpass456"` |
| `flask create-student <degree> <courses> <gpa> <password>` | Create a new student record. | `flask create-student "Computer Science" "COMP2601,COMP3602" 3.8 "studpass789"` |

---

### Employer Commands (Group: `flask employer`)

These commands are prefixed with `flask employer`. They are used by employers to manage their internship postings and shortlists.

| Command | Description | Arguments |
| :--- | :--- | :--- |
| `create-internship` | Creates a new internship posting for a specified employer. | `<title> <details> <employer_id>` |
| `view-internships` | View all internships posted by a specific employer. | `<employer_id>` |
| `delete-internship` | Deletes an internship posting after prompting the user to select from the employer's list. | `<employer_id>` |
| `update-internship` | Updates the title, details, and/or status of an existing internship after prompting the user to select from the employer's list. | `<employer_id>` |
| `view-internship-shortlist` | View the shortlist of students for a specific internship posting. | `<employer_id> <internship_id>` |
| `update-shortlist-status` | Updates the status of a specific student's entry on an internship's shortlist. | `<employer_id> <internship_id>` |

**Example Usage:**

```bash
# Create an internship for the employer with ID 1
flask employer create-internship "Web Dev Intern" "Develop and maintain company website." 1

# View all internships posted by employer with ID 1
flask employer view-internships 1
```

---

### Staff Commands (Group: `flask staff`)

These commands are prefixed with `flask staff`. They are used by staff members for system-wide viewing and creating shortlist entries.

| Command | Description | Arguments |
| :--- | :--- | :--- |
| `view-all-internships` | View all internship postings across all employers.. | None |
| `view-all-students` | View all registered student profiles. | None |
| `create-shortlist-position` | Creates a shortlist entry, placing a specified student on a specified internship's shortlist. | `<staff_id><student_id>` |

**Example Usage:**

```bash
# View all available internships
flask staff view-all-internships

# Staff member (ID 2) shortlists student (ID 3) for an internship (will prompt for internship_id)
flask staff create-shortlist-position 2 3
```
---

### Student Commands (Group: `flask student`)

These commands are prefixed with `flask student`. They are used by students to view their application and shortlist status.

| Command | Description | Arguments |
| :--- | :--- | :--- |
| `view-shortlisted-positions` | View all internships for which the student has been shortlisted. | `<student_id>` |

**Example Usage:**

```
# View shortlisted positions for the student with ID 3
flask student view-shortlisted-positions 3
```
