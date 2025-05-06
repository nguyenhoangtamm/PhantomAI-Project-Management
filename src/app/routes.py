from flask import Blueprint, render_template, request, jsonify,redirect,url_for
from app.models import Employee, Project, Skill, EmployeeSkill,Role
from app import db
from flask import Blueprint, render_template, request, jsonify
from app.services.project_analysis import analyze_project_requirements
from app.services.resource_allocation import allocate_resources
import os
from dotenv import load_dotenv
main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@main.route("/ai")
def ai():
    projects = Project.query.all()
    return render_template("ai.html", projects=projects)

@main.route("/suggest", methods=["POST"])
def phantomai():
    load_dotenv()
    together_api_key = os.getenv("TOGETHER_API_KEY", "20ec9bc306ec0bed85ec37e0d9db9d414c81701d272c6310e8287381f01cae26")

    # Phân tích yêu cầu dự án
    project_id = request.form.get("project")
    project_analysis = analyze_project_requirements(project_id)
    
    return allocate_resources(project_analysis)
    # return jsonify(project_analysis), 200

#@main.route("/employee")
@main.route("/employee")
def list_employees():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)


@main.route("/employee/add", methods=["POST"])
def add_employee():
    try:
        fullname = request.form.get("fullname")
        position = request.form.get("position")
        if not fullname or not position:
            return jsonify({"error": "Fullname and position are required."}), 400

        new_employee = Employee(fullname=fullname, position=position)
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"message": "Employee added successfully."}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@main.route("/employee/update/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found."}), 404

        fullname = request.form.get("fullname")
        position = request.form.get("position")
        if fullname:
            employee.fullname = fullname
        if position:
            employee.position = position

        db.session.commit()
        return jsonify({"message": "Employee updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@main.route("/employee/delete/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found."}), 404

        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Employee deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


## project
@main.route("/project")
def project():
    projects = Project.query.order_by(Project.id.asc()).all()


    return render_template("project.html", projects=projects)

@main.route("/project/add", methods=["POST"])
def add_project():
    try:
        name = request.form.get("name")
        description = request.form.get("description")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        duration = request.form.get("duration")
        status = request.form.get("status")
        projectcost = request.form.get("projectcost")

        # Tạo đối tượng Project mới
        new_project = Project(
            name=name,
            description=description,
            startdate=startdate,
            enddate=enddate if enddate else None,
            duration=duration,
            status=status,
            projectcost=projectcost
        )

        db.session.add(new_project)
        db.session.commit()

        return render_template("project.html", projects=Project.query.all())

    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}", 500
    
@main.route('/project/<int:project_id>')
def project_details(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("details.html", project=project)


@main.route('/project/edit/<int:id>')
def edit_project(id):
    project = Project.query.get_or_404(id)
    return render_template('edit_project.html', project=project)

# Sửa dự án
@main.route('/project/update/<int:id>', methods=['POST'])
def update_project(id):
    project = Project.query.get_or_404(id)
    project.name = request.form['name']
    project.description = request.form['description']
    project.startdate = request.form['start_date']
    project.enddate = request.form['end_date']
    project.duration = request.form['duration']
    project.status = request.form['status']
    project.projectcost = request.form['cost']

    db.session.commit()
    return redirect(url_for('main.home'))  # hoặc 'main.project_list' nếu bạn có view đó 

@main.route("/project/delete/<int:id>", methods=["POST"])
def delete_project(id):
    project = Project.query.get_or_404(id)
    try:
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('main.home'))
    except Exception as e:
        return f"Lỗi khi xóa: {str(e)}", 500

