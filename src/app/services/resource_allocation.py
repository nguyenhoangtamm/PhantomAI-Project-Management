import re
from flask import jsonify
from app.models import Role, Employee, Project, Technology, EmployeeProject, ProjectTechnology,EmployeeSkill, Skill
from app.services.utils import call_api
from dotenv import load_dotenv
import os
import json

load_dotenv()
together_api_key = os.getenv("TOGETHER_API_KEY", "20ec9bc306ec0bed85ec37e0d9db9d414c81701d272c6310e8287381f01cae26")

def allocate_resources(project_id):
    employee_list = Employee.query.all()
    empl_for_prompt = []
    for emp in employee_list:
        emp_skills = EmployeeSkill.query.filter_by(employeeid=emp.id).all()
        emp_skills_list = []
        for emp_skill in emp_skills:
            skill = Skill.query.get(emp_skill.skillid)
            if skill:
                emp_skills_list.append(skill.name)
        empl_for_prompt.append({
            "id": emp.id,
            "name": emp.fullname,
            "skills": emp_skills_list
        })
    if not employee_list:
        return jsonify({"error": "No employees available for allocation."}), 400    
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"error": "Project does not exist."}), 400
    project_technology = ProjectTechnology.query.filter_by(projectid=project.id).all()
    if not project_technology:
        return jsonify({"error": "Project does not have any technology."}), 400
    roles = Role.query.all()
    tec_name = ""
    for tec_id in project_technology:
        technology = Technology.query.get(tec_id.technologyid)
        if technology:
            tec_name += technology.name + ", "
    tec_name = tec_name[:-2]  # Remove the last comma and space
    role_requirements = suggest_required_employees(project, roles,tec_name)

    result = []
    max_retries = 10
    for attempt in range(max_retries):
        

        prompt = f"""
        Project: {project.name}
        Description: {project.description}
        Technologies: {tec_name}
        Roles and their requirements:
        {role_requirements}
        Employee list: {empl_for_prompt}
        Please allocate resources for this project.
        Return a list of employee IDs that are most suitable for this role based on their skills and the project requirements.
        JSON format:
        [{{ "role_id": 1, "employee_ids": [1, 2, 3] }},{{ "role_id": 2, "employee_ids": [4, 5] }},...]
        Only return the requested data without any additional descriptions or explanations.
            Only return JSON without any additional text.
        """
        headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.85,
        }
        # Call the AI API with the generated prompt
        response = call_api(headers, data)
        suggestions = response.get("choices", [{}])[0].get("text", "").strip()
        pattern = r'\{[^}]*"role_id"[^}]*"employee_ids"[^}]*\}'
        matches = re.findall(pattern, suggestions)
        if matches:
    # Chuyển đổi từng chuỗi JSON thành Python dict
            result = [json.loads(match) for match in matches]
            return result
        else:
            raise ValueError("No valid JSON objects found in response")
    
           

    return jsonify(result), 200
        
        
        

    


def suggest_required_employees(project, roles, technologies, max_retries=10):
    """
    Call AI to suggest the required number of employees for all roles in the roles list for the project.
    If the returned data is invalid, retry calling the API up to max_retries times.
    """
    roles_prompt = "\n".join([f"- Role: {role.name}" for role in roles])
    prompt = f"""
    Project: {project.name}
    Description: {project.description}
    Technologies: {technologies}
    Required roles:
    {roles_prompt}
    Please suggest the required number of employees for each role in the project.
    Return the list of required employees in JSON format as follows:
    [
        {{ "role_id": 1, "role_name": "Developer", "suggested_count": 3 }},
        {{ "role_id": 2, "role_name": "Designer", "suggested_count": 2 }}
    ]
    Only return the requested data without any additional descriptions or explanations.
    """
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 2000,
        "temperature": 0.7,
        "top_p": 0.85,
    }

    for attempt in range(max_retries):
        try:
            response = call_api(headers, data)
            suggestions = response.get("choices", [{}])[0].get("text", "").strip()

            # Find the JSON list in the response
            start_idx = suggestions.find("[")
            end_idx = suggestions.find("]", start_idx) + 1
            if start_idx != -1 and end_idx != -1:
                employee_counts_str = suggestions[start_idx:end_idx]
                # Convert the JSON string to a Python list
                import json
                employee_counts = json.loads(employee_counts_str)
            else:
                raise ValueError("No valid list found in response")
            
            # Validate the format of each item in the list
            if not isinstance(employee_counts, list):
                raise ValueError("Invalid response format: Not a list")
            for item in employee_counts:
                if not isinstance(item, dict) or "role_id" not in item or "role_name" not in item or "suggested_count" not in item:
                    raise ValueError("Invalid response format: Missing required keys")
            
            # If the data is valid, return the result
            role_requirements = []
            for role in roles:
                # Find the corresponding role in the response
                matching_role = next((item for item in employee_counts if item["role_id"] == role.id), None)
                if matching_role:
                    role_requirements.append({
                        "role_id": role.id,
                        "role_name": role.name,
                        "suggested_count": matching_role["suggested_count"]
                    })
                else:
                    role_requirements.append({
                        "role_id": role.id,
                        "role_name": role.name,
                        "suggested_count": "Not specified"
                    })
            return role_requirements

        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                # If max retries are reached, return default values
                print("Max retries reached. Returning default values.")
                return [{"role_id": role.id, "role_name": role.name, "suggested_count": "Not specified"} for role in roles]

    # In case no valid response is received after all retries
    return [{"role_id": role.id, "role_name": role.name, "suggested_count": "Not specified"} for role in roles]


