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
       

    return {
        "project_name": project.name,
        "description": project.description,
        "cost": response.get("development_cost"),
        "duration": response.get("time_estimate"),
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











