from app import db

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    position = db.Column(db.String(50), nullable=False)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    project_cost = db.Column(db.Numeric(15, 2), nullable=False)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class EmployeeAssignment(db.Model):
    __tablename__ = 'employee_assignment'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    hours_worked = db.Column(db.Integer, nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)


class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class EmployeeSkill(db.Model):
    __tablename__ = 'employee_skill'
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    proficiency_level = db.Column(db.String(50), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
