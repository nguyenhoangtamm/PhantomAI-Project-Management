from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Tạo instance của SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Nạp cấu hình từ file config.py

    db.init_app(app)  # Khởi tạo SQLAlchemy với ứng dụng Flask

    with app.app_context():
        db.create_all()  # Tạo các bảng trong cơ sở dữ liệu nếu chưa tồn tại

    # Import Blueprint sau khi db đã được khởi tạo
    from app.routes import main
    app.register_blueprint(main)

    return app