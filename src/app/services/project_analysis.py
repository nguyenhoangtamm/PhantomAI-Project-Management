from app.models import Project, Role,Technology
from app.services.utils import call_api
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()
together_api_key = os.getenv("TOGETHER_API_KEY", "20ec9bc306ec0bed85ec37e0d9db9d414c81701d272c6310e8287381f01cae26")

def analyze_project_requirements(project_id, technologies):
    
    project = Project.query.get(project_id)
    if not project:
        return {"error": "Project does not exist."}
    tec_name = []
    for tec_id in technologies:
        technology = Technology.query.get(int(tec_id))
        if technology:
            tec_name.append(technology.name)
    tec_name = ", ".join(tec_name)

    # Phân tích chi phí
    response = suggest_project_cost_duration(project,tec_name)
    roles = Role.query.all()
    role_requirements = suggest_required_employees(project, roles,tec_name)
       

    return {
        "project_name": project.name,
        "description": project.description,
        "cost": response.get("development_cost"),
        "duration": response.get("time_estimate"),
        "role_requirements": role_requirements,
    }

def suggest_project_cost_duration(project,technologies):
    """
    Gọi AI để gợi ý chi phí cho dự án.
    """
    prompt = f"""
Project: {project.name}
Description: {project.description}
Technologies: {technologies}
Return a JSON in the following format:
{{
    "time_estimate": <time required (in months)>,
    "development_cost": <development cost (in VND)>
}}
Do not include any units or additional text, only integers.
Only return the JSON. Do not include any other text.
"""
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.85,
    }
    max_retries = 10
    result = None
    for attempt in range(max_retries):
        response = call_api(headers, data)
        # Tìm giá trị trong cặp {}
        detec= response.get("choices", [{}])[0].get("text", "Không xác định").strip()
        json_response = re.findall(r'\{[^}]*\}', detec)

        if json_response:
            json_object = json.loads(json_response[0])  # Convert the first match to a JSON object
            print(f"JSON Object: {json_object}")
            # Kiểm tra xem các trường có kiểu dữ liệu hợp lệ không
            if "time_estimate" in json_object and "development_cost" in json_object:
                if isinstance(json_object["time_estimate"], int) and isinstance(json_object["development_cost"], int):
                    # Nếu kiểu dữ liệu hợp lệ, trả về kết quả
                    if json_object["time_estimate"] > 0 and json_object["development_cost"] > 0:
                        result = {
                            "time_estimate": json_object["time_estimate"],
                            "development_cost": json_object["development_cost"]
                        }
                        break
    print("result:", result)    
    return result




def suggest_required_employees(project, roles, technologies, max_retries=10):
    """
    Gọi AI để gợi ý số lượng nhân lực cần thiết cho tất cả các vai trò trong danh sách roles của dự án.
    Nếu dữ liệu trả về không hợp lệ, thử gọi lại API tối đa max_retries lần.
    """
    roles_prompt = "\n".join([f"- Vai trò: {role.name}" for role in roles])
    prompt = f"""
    Dự án: {project.name}
    Mô tả: {project.description}
    Các công nghệ: {technologies}
    Các vai trò cần thiết:
    {roles_prompt}
    Hãy gợi ý số lượng nhân lực cần thiết cho từng vai trò trong dự án,
    Trả về danh sách số lượng nhân lực dưới dạng JSON như sau:
    [
        {{ "role_id": 1, "role_name": "Developer", "suggested_count": 3 }},
        {{ "role_id": 2, "role_name": "Designer", "suggested_count": 2 }}
    ]
    Chỉ cần trả những thứ yêu cầu không cần mô tả và giải thích.
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
            # print(f"Attempt {attempt + 1}: {suggestions}")  # In ra phản hồi để kiểm tra

            # Tìm giá trị trong cặp []
            start_idx = suggestions.find("[")
            end_idx = suggestions.find("]", start_idx) + 1
            if start_idx != -1 and end_idx != -1:
                employee_counts_str = suggestions[start_idx:end_idx]
                # Chuyển đổi chuỗi JSON thành danh sách Python
                import json
                employee_counts = json.loads(employee_counts_str)
            else:
                raise ValueError("No valid list found in response")
            
            # Kiểm tra định dạng của từng phần tử trong danh sách
            if not isinstance(employee_counts, list):
                raise ValueError("Invalid response format: Not a list")
            for item in employee_counts:
                if not isinstance(item, dict) or "role_id" not in item or "role_name" not in item or "suggested_count" not in item:
                    raise ValueError("Invalid response format: Missing required keys")
            
            # Nếu dữ liệu hợp lệ, trả về kết quả
            role_requirements = []
            for role in roles:
                # Tìm vai trò tương ứng trong phản hồi
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
                        "suggested_count": "Không xác định"
                    })
            return role_requirements

        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                # Nếu hết số lần thử, trả về danh sách mặc định
                print("Max retries reached. Returning default values.")
                return [{"role_id": role.id, "role_name": role.name, "suggested_count": "Không xác định"} for role in roles]

    # Trường hợp không có phản hồi hợp lệ sau tất cả các lần thử
    return [{"role_id": role.id, "role_name": role.name, "suggested_count": "Không xác định"} for role in roles]












