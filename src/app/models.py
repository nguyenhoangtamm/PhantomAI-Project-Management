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
    duration = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    projectcost = db.Column(db.Numeric(15, 2), nullable=False)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


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


class EmployeeProject(db.Model):
    __tablename__ = 'employee_project'
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    projectid = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    roleid = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    startdate = db.Column(db.Date, nullable=False)
    enddate = db.Column(db.Date, nullable=True)
    salary = db.Column(db.Numeric(15, 2), nullable=False)


class Technology(db.Model):
    __tablename__ = 'technology'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class ProjectTechnology(db.Model):
    __tablename__ = 'project_technology'
    projectid = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    technologyid = db.Column(db.Integer, db.ForeignKey('technology.id'), primary_key=True)
