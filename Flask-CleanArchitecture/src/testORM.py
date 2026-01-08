from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse

# 1. Cấu hình kết nối (Theo đúng lệnh Docker bạn đã chạy)
# Lưu ý: 'localhost' vì Docker đã map port 1433 ra máy thật
server = 'localhost' 
database = 'master'  # Dùng tạm database master để test
username = 'sa'
password = 'Aa123456'
driver = 'ODBC Driver 17 for SQL Server' # Hoặc 'ODBC Driver 18...' tùy máy bạn

# Tạo chuỗi kết nối an toàn
params = urllib.parse.quote_plus(
    f'DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
)
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

# 2. Khởi tạo Engine
try:
    engine = create_engine(connection_string)
    connection = engine.connect()
    print("✅ KẾT NỐI THÀNH CÔNG ĐẾN MS SQL SERVER!")
    connection.close()
except Exception as e:
    print("❌ Lỗi kết nối:", e)
    exit() # Dừng luôn nếu không kết nối được

# 3. Định nghĩa Model (ORM) - Thử tạo 1 bảng User giả
Base = declarative_base()

class TestUser(Base):
    __tablename__ = 'test_users' # Tên bảng trong SQL sẽ là test_users
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))

# 4. Thực thi ORM (Tạo bảng)
print("⏳ Đang tạo bảng 'test_users' từ code Python...")
Base.metadata.create_all(engine)
print("✅ Đã tạo bảng thành công!")

# 5. Thử thêm dữ liệu (Insert)
Session = sessionmaker(bind=engine)
session = Session()

new_user = TestUser(name="Nguyen Van A", email="test@gmail.com")
session.add(new_user)
session.commit()
print("✅ Đã thêm user 'Nguyen Van A' vào database!")

# 6. Thử lấy dữ liệu ra (Select)
user = session.query(TestUser).filter_by(name="Nguyen Van A").first()
print(f"🔍 Đọc từ Database: ID={user.id}, Name={user.name}, Email={user.email}")