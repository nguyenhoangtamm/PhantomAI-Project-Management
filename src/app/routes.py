from flask import Blueprint, render_template, request, jsonify
from app.models import NhanVien
from app import db

from app.models import DuAn
from app.models import Kynang
from app.models import Nhanvien_kynang
import os
from dotenv import load_dotenv
import requests

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    nhanvien= NhanVien.query.all()

    return render_template("index.html", nhanvien=nhanvien)

@main.route("/ai")
def ai():
    projects = DuAn.query.all()
   
    return render_template("ai.html",projects= projects)
@main.route("/suggest", methods=["POST"])
def phantomai():
    load_dotenv()
    together_api_key = os.getenv("TOGETHER_API_KEY")

    """Xử lý yêu cầu phân bổ nguồn lực."""
    try:
        # Lấy dữ liệu từ form
        project_id = request.form.get("project")
        print(project_id)
        project = DuAn.query.get(project_id)
        print(project_id)
        if not project:
            return jsonify({"error": "Dự án không tồn tại."}), 400
        description = project.mota
        nhanviens =NhanVien.query.all()
        # Tạo danh sách nhân viên và kỹ năng của họ
        members = []
        for nhanvien in nhanviens:
            skills = db.session.query(Kynang.tenkynang, Nhanvien_kynang.mucdothanhthao, Nhanvien_kynang.sonamkinhnghiem).join(
            Nhanvien_kynang, Kynang.makynang == Nhanvien_kynang.makynang
            ).filter(Nhanvien_kynang.manv == nhanvien.manv).all()
            skill_details = ", ".join(
            [f"{skill[0]} (Mức độ: {skill[1]}, Kinh nghiệm: {skill[2]} năm)" for skill in skills]
            )
            members.append(f"{nhanvien.hoten} - {nhanvien.chucvu} - Kỹ năng: {skill_details}")

        members = "\n".join(members)

        # Tạo danh sách công việc từ mô tả dự án
        prompt = f"""
Bạn là một hệ thống AI hỗ trợ quản lý dự án.
Hãy dựa vào danh sách nhân viên và mô tả dự án dưới đây để phân bổ nguồn lực phù hợp.

Nhân viên:
{members}

Dự án:
{description}

Trả lời theo định dạng:
- Công việc: (tên công việc)
- Người đề xuất: (tên người thực hiện)
- Lý do: (lý do phân bổ)
"""

        # Cấu hình header và payload cho API
        headers = {
            "Authorization": f"Bearer {together_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 1500,  # Giảm số lượng token để tránh vượt quá giới hạn
            "temperature": 0.7,
            "top_p": 0.85,  # Điều chỉnh để tăng tính đa dạng của phản hồi
        }

        # Gửi yêu cầu đến Together AI
        response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=data,timeout=20)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        # Xử lý phản hồi từ API
        response_data = response.json()
        if "choices" in response_data and response_data["choices"]:
            suggestion = response_data["choices"][0]["text"]
            return jsonify({"result": suggestion})
        else:
            return jsonify({"error": "Không nhận được phản hồi từ Together AI."}), 500

    except requests.exceptions.RequestException as e:
        # Xử lý lỗi khi gọi API
        return jsonify({"error": f"Lỗi khi gọi Together AI: {str(e)}"}), 500
    except Exception as e:
        # Xử lý lỗi chung
        return jsonify({"error": f"Đã xảy ra lỗi: {str(e)}"}), 500