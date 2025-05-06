import re
from flask import jsonify
from app.models import Role, Employee
from app.services.utils import call_api
from dotenv import load_dotenv
import os

load_dotenv()
together_api_key = os.getenv("TOGETHER_API_KEY", "20ec9bc306ec0bed85ec37e0d9db9d414c81701d272c6310e8287381f01cae26")

def allocate_resources(project_analysis):
    employee_list = Employee.query.all()
    if not employee_list:
        return jsonify({"error": "No employees available for allocation."}), 400    
    
    if "error" in project_analysis:
        return jsonify(project_analysis), 400

    # # Tạo prompt cho AI
    prompt = f"""
    Dự án: {project_analysis}
    Hãy phân bổ nhân lực cho dự án này.
    Đưa ra lý do cho mỗi sự phân bổ.
    Định dạng JSON.
    Ví dụ:
    [
        (1, 2, "Lý do phân bổ nhân viên 2 cho vai trò 1"),
        (2, 3, "Lý do phân bổ nhân viên 3 cho vai trò 2"),
        (3, 4, "Lý do phân bổ nhân viên 4 cho vai trò 3")
    ]
        Chỉ cần trả về JSON mà không có bất kỳ văn bản nào khác.

    """

    # Gọi API và phân bổ nhân lực
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
    }
    # roles = Role.query.all()

    # max_retries = 10
    # for attempt in range(max_retries):
    #     try:
    #         list_detail = []
    #         response_data = call_api(data, headers)
    #         if "choices" in response_data and response_data["choices"]:
    #             suggestion = response_data["choices"][0]["text"]
    #             extracted_suggestion = re.findall(r"\(.*?\)", suggestion, re.DOTALL)

    #             for suggestion in extracted_suggestion:
    #                 cleaned_suggestion = suggestion.strip("()")
    #                 parts = cleaned_suggestion.split(",")
    #                 if len(parts) != 3:
    #                     continue
    #                 part_json = {
    #                     "task_id": int(parts[0].strip()),
    #                     "employee_id": int(parts[1].strip()),
    #                     "reason": parts[2].strip().strip('"')
    #                 }
    #                 list_detail.append(part_json)

    #             if not list_detail or len(list_detail) < len(roles):
    #                 continue

    #             return jsonify({"result": list_detail})
    #     except Exception as e:
    #         if attempt == max_retries - 1:
    #             return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    # return jsonify({"error": "No valid response from Together AI after retries."}), 500

    response = call_api(headers, data)
    if "choices" in response and response["choices"]:
        suggestion = response["choices"][0]["text"]
        print("Suggestion:", suggestion)
        extracted_suggestion = re.findall(r"\(.*?\)", suggestion, re.DOTALL)

        # list_detail = []
        # for suggestion in extracted_suggestion:
        #     cleaned_suggestion = suggestion.strip("()")
        #     parts = cleaned_suggestion.split(",")
        #     # if len(parts) != 3:
        #     #     continue
        #     part_json = {
        #         "role_id": int(parts[0].strip()),
        #         "employee_id": int(parts[1].strip()),
        #         "reason": parts[2].strip().strip('"')
        #     }
        #     list_detail.append(part_json)

        # if not list_detail or len(list_detail) < len(employee_list):
        #     return jsonify({"error": "Not enough valid allocations."}), 400

        return jsonify({"result": extracted_suggestion}), 200

