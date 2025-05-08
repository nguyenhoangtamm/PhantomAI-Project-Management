from flask import Blueprint, render_template, request, jsonify,redirect,url_for
from app.models import Employee, Project, Skill, EmployeeSkill,Role,ProjectTechnology,Technology,EmployeeProject
from app import db
from flask import Blueprint, render_template, request, jsonify
from app.services.project_analysis import analyze_project_requirements
from app.services.resource_allocation import allocate_resources
import os
from datetime import datetime as Datetime
from dotenv import load_dotenv
import traceback
main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@main.route("/employee")
def list_employees():
    employees = Employee.query.all()
    return render_template("employee/employee.html", employees=employees)


@main.route("/employee/add", methods=["POST"])
def add_employee():
    try:
        fullname = request.form.get("fullname")
        position = request.form.get("position")
        dateofbirth = request.form.get("dateofbirth")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phonenumber = request.form.get("phonenumber")

        if not dateofbirth or not gender or not email or not phonenumber:
            return jsonify({"error": "Date of birth, gender, email, and phone number are required."}), 400
        if not fullname or not position:
            return jsonify({"error": "Fullname and position are required."}), 400

        new_employee = Employee(
                fullname=fullname,
                position=position,
                dateofbirth=dateofbirth,
                gender=gender,
                email=email,
                phonenumber=phonenumber
            )
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for("main.list_employees"))
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@main.route('/employee/edit/<int:id>')
def edit_employee(id):
    """
    Hiển thị giao diện chỉnh sửa dự án.
    """
    employee = Employee.query.get_or_404(id)
    return render_template('employee/edit_employee.html', employee=employee)



@main.route("/employee/update/<int:employee_id>", methods=["POST"])
def update_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)

        fullname = request.form.get("fullname")
        position = request.form.get("position")
        dateofbirth = request.form.get("dateofbirth")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phonenumber = request.form.get("phonenumber")

        if not dateofbirth or not gender or not email or not phonenumber:
            return jsonify({"error": "Date of birth, gender, email, and phone number are required."}), 400
        if not fullname or not position:
            return jsonify({"error": "Fullname and position are required."}), 400

        employee.fullname = fullname
        employee.position = position
        employee.dateofbirth = dateofbirth
        employee.gender = gender
        employee.email = email
        employee.phonenumber = phonenumber

        db.session.commit()
        return redirect(url_for("main.list_employees"))
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@main.route("/employee/delete/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for("main.list_employees"))
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

## project
@main.route("/project")
def project():
    """
    Hiển thị danh sách các dự án.
    """
    projects = Project.query.order_by(Project.id.asc()).all()
    return render_template("project/project.html", projects=projects)


@main.route("/project/add", methods=["POST"])
def add_project():
    """
    Thêm một dự án mới.
    """
    try:

        name = request.form.get("name")
        description = request.form.get("description")
        if request.form.get("startdate"):
            startdate = request.form.get("startdate")
        else:
            startdate = Datetime.now().date()
        enddate = request.form.get("enddate")
        
        if request.form.get("duration"):
            duration = request.form.get("duration")
        else:
            duration = 0
        status = request.form.get("status")
        if  request.form.get("projectcost"):
            projectcost = request.form.get("projectcost")
        else:
            projectcost = 0


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

        return render_template("project/project.html", projects=Project.query.all())

    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}", 500


@main.route('/project/<int:project_id>')
def project_details(project_id):
    """
    Hiển thị chi tiết một dự án.
    """
    project = Project.query.get_or_404(project_id)
    technologies = Technology.query.join(ProjectTechnology, Technology.id == ProjectTechnology.technologyid)\
                                   .filter(ProjectTechnology.projectid == project_id).all()
    employee= Employee.query.join(EmployeeProject, Employee.id == EmployeeProject.employeeid)
    employee=employee.filter(EmployeeProject.projectid == project_id).all()

    return render_template('project/details.html', project=project, technologies=technologies, employee=employee)


@main.route('/project/edit/<int:id>')
def edit_project(id):
    """
    Hiển thị giao diện chỉnh sửa dự án.
    """
    project = Project.query.get_or_404(id)
    return render_template('project/edit_project.html', project=project)


@main.route('/project/update/<int:id>', methods=['POST'])
def update_project(id):
    """
    Cập nhật thông tin dự án.
    """
    project = Project.query.get_or_404(id)
    project.name = request.form['name']
    project.description = request.form['description']
    project.startdate = request.form['start_date']
    project.enddate = request.form['end_date']
    project.duration = request.form['duration']
    project.status = request.form['status']
    project.projectcost = request.form['cost']

    db.session.commit()
    return redirect(url_for('main.project'))


@main.route("/project/delete/<int:id>", methods=["POST"])
def delete_project(id):
    """
    Xóa một dự án.
    """
    project = Project.query.get_or_404(id)
    try:
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('main.project'))
    except Exception as e:
        return f"Lỗi khi xóa: {str(e)}", 500

@main.route("/project/allocation_project/<int:project_id>")
def allocation_project(project_id):
    """
    Hiển thị chi tiết phân bổ nhân lực cho dự án.
    """
    project = Project.query.get_or_404(project_id)
    technologies = Technology.query.all()

    return render_template("allocation/allocation_project.html", project=project, technologies=technologies)



## phan bo

@main.route("/suggest", methods=["POST"])
def phantomai():
    load_dotenv()
    # Phân tích yêu cầu dự án
    project_id = request.form.get("project_id")
    technologies = request.form.get("selectedTechnologies")
    technologies = technologies.strip("[]").replace('"', '').split(",") if technologies else []
    project_analysis = analyze_project_requirements(project_id, technologies)
    return project_analysis
   
@main.route("/add-allocation-project", methods=["POST"])
def add_allocation_project():
    """
    Thêm phân bổ nguồn lực cho dự án.
    """
    try:
        data = request.get_json()  # Lấy dữ liệu JSON từ request

        project_id = data.get("project_id")
        technology_ids = data.get("technologies", [])
        project_cost = data.get("project_cost")
        project_duration = data.get("project_duration")

        # Update project details with cost and duration
        project = Project.query.get_or_404(project_id)
        project.projectcost = project_cost
        project.duration = project_duration
        db.session.commit()
        # xoá tất cả các công nghệ cũ liên quan đến dự án
        ProjectTechnology.query.filter_by(projectid=project_id).delete()
        for technology_id in technology_ids:
            project_technology = ProjectTechnology(
                projectid=project_id,
                technologyid=technology_id
            )
            db.session.add(project_technology)
        
        db.session.commit()
        
        return redirect(url_for("main.project_details", project_id=project_id))
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}", 500
    


@main.route("/allocation_project_emplyee/<int:project_id>")
def allocation_project_emplyee(project_id):
    """
    Phân bổ nhân lực cho dự án.
    """
    project = Project.query.get_or_404(project_id)
    allocation_result = allocate_resources( project_id)
    # Convert employee_ids to employee objects
    formatted_allocation_result = []
    for allocation in allocation_result:
        role_id = allocation.get("role_id")
        role = Role.query.get(role_id) if role_id else None
        employee_ids = allocation.get("employee_ids", [])
        employees = Employee.query.filter(Employee.id.in_(employee_ids)).all()
        formatted_allocation_result.append({
            "role": role,
            "employees": employees
        })

    allocation_result = formatted_allocation_result

    return render_template("allocation/allocation_employee.html", project=project, allocation_result=allocation_result)



@main.route("/save-allocation", methods=["POST"])
def save_allocation():
    """
    API để lưu thông tin phân bổ nhân lực và dự án.
    """
    try:
        data = request.get_json()
        project_id = data.get("project_id")
        allocation_data = data.get("allocations")

        # Xử lý dữ liệu dự án

        # Xử lý dữ liệu phân bổ
        for allocation in allocation_data:
            role_id = allocation.get("role")
            employee_ids = allocation.get("employees", [])
            start_date = allocation.get("start_date") or Datetime.now().date()
            end_date = allocation.get("end_date") or None
            salary = 0

            for employee_id in employee_ids:
                # Thêm dữ liệu vào bảng EmployeeProject
                # Kiểm tra xem bản ghi đã tồn tại trong cơ sở dữ liệu chưa
                existing_record = EmployeeProject.query.filter_by(
                    employeeid=int(employee_id),
                    projectid=int(project_id),
                    roleid=int(role_id)
                ).first()

                if not existing_record:
                    # Nếu chưa tồn tại, thêm bản ghi mới
                    employee_project = EmployeeProject(
                        employeeid=int(employee_id),
                        projectid=int(project_id),
                        roleid=int(role_id),
                        startdate=start_date,
                        enddate=end_date,
                        salary=float(salary)
                    )
                    db.session.add(employee_project)

        db.session.commit()

        return jsonify({"success": True}), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500