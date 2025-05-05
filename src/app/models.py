from app import db

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    dateofbirth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phonenumber = db.Column(db.String(15), nullable=False)
    position = db.Column(db.String(50), nullable=False)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    startdate = db.Column(db.Date, nullable=False)
    enddate = db.Column(db.Date, nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    projectcost = db.Column(db.Numeric(15, 2), nullable=False)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class EmployeeAssignment(db.Model):
    __tablename__ = 'employee_assignment'
    id = db.Column(db.Integer, primary_key=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    roleid = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    hoursworked = db.Column(db.Integer, nullable=False)
    hourlyrate = db.Column(db.Numeric(10, 2), nullable=False)


class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class EmployeeSkill(db.Model):
    __tablename__ = 'employee_skill'
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    skillid = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    proficiencylevel = db.Column(db.String(50), nullable=False)
    yearsofexperience = db.Column(db.Integer, nullable=False)
