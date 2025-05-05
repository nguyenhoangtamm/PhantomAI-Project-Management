from flask import Blueprint, render_template, request, jsonify
from app.models import Employee, Project, Skill, EmployeeSkill,Role
from app import db
import os
from dotenv import load_dotenv
import requests

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
    # together_api_key = os.getenv("TOGETHER_API_KEY")
    together_api_key = "20ec9bc306ec0bed85ec37e0d9db9d414c81701d272c6310e8287381f01cae26"
    """
# Trả lời theo định dạng:
#         - Nhiệm vụ: (tên nhiệm vụ)
#         - Nhân viên được đề xuất: (nhân viên)
#         - Lý do: (lý do phân bổ)
#         """
    try:
        # Get project ID from form
        project_id = request.form.get("project")
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Project does not exist."}), 400

        description = project.description
        employees = Employee.query.all()
        roles = Role.query.all()
        # Get the roles and their descriptions
        rolemessages = []
        for role in roles:
            rolemessages.append(f"{role.id}: {role.name}")

        # Create a list of employees and their skills
        members = []
        for employee in employees:
            skills = db.session.query(Skill.name, EmployeeSkill.proficiencylevel, EmployeeSkill.yearsofexperience).join(
                EmployeeSkill, Skill.id == EmployeeSkill.skillid
            ).filter(EmployeeSkill.employeeid == employee.id).all()
            skill_details = ", ".join(
                [f"{skill[0]} (Proficiency: {skill[1]}, Experience: {skill[2]} years)" for skill in skills]
            )
            members.append(f"id: {employee.id} - {employee.fullname} - {employee.position} - Skills: {skill_details}")

        members = "\n".join(members)

        # Create the prompt for the AI
        prompt = f"""
        Bạn là một hệ thống AI hỗ trợ quản lý dự án.
        Dựa trên danh sách nhân viên và mô tả dự án dưới đây, hãy phân bổ nguồn lực một cách hợp lý.

        Nhân viên:
        {members}

        Vai trò:
        {rolemessages}

        Dự án:
        {description}

        Trả lời theo định dạng JSON thuần túy:
        (id nhiệm vụ), (id nhân viên), (lý do phân bổ)
        ví dụ:
        (1, 2, "Nhân viên này có kỹ năng phù hợp với nhiệm vụ và đã làm việc trong dự án tương tự trước đây.")
        lưu ý rằng 1 nhiệm vụ có thể được phân bổ cho nhiều nhân viên khác nhau, và 1 nhân viên chỉ có thể đảm nhiệm 1 nhiệm vụ duy nhất.
        """
        # Configure headers and payload for the API
        headers = {
            "Authorization": f"Bearer {together_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "prompt": prompt,
            "max_tokens": 2500,
            "temperature": 0.7,
            "top_p": 0.85,
            # "stop": ["\n\n"]
        }

        # Send request to Together AI
        response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=data, timeout=20)
        response.raise_for_status()

        # Process the API response
        response_data = response.json()
        if "choices" in response_data and response_data["choices"]:
            suggestion = response_data["choices"][0]["text"]
            # Clean up the suggestion text
            
            return jsonify({"result": suggestion})
        else:
            return jsonify({"error": "No response from Together AI."}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error calling Together AI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


