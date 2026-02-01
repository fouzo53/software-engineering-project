from dotenv import load_dotenv
import sys
import os

# Thêm src vào Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

load_dotenv()

from src.create_app import create_app
from src.infrastructure.databases.database import db

app = create_app()

# Tạo bảng database
with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully!")

if __name__ == "__main__":
    print("Starting BizFlow API on http://0.0.0.0:6868")
    print("Swagger docs: http://localhost:6868/docs")
    app.run(host="0.0.0.0", port=6868, debug=True)
