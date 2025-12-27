---
tags:
  - sprint-2
  - bizflow
  - clean-architecture
  - docker
  - authentication
status: Planning
---

# 🚀 Sprint 2: Foundation & Authentication

**Mục tiêu chính:**
1.  Thiết lập môi trường phát triển chuẩn **Docker** (Backend + Database).
2.  Xây dựng khung Backend theo **Clean Architecture**.
3.  Hoàn thiện tính năng **Đăng nhập (Login)** End-to-End (Mobile/Web <-> API <-> Database).

---

## 1. Phân công nhiệm vụ (Task Breakdown)

### 👑 Quản lý & Review (Leader)
*   **Assignee:** **Xuân Huy**
*   **Tasks:**
    *   [MGMT] Khởi tạo Repo mới (hoặc nhánh `feature/clean-arch`), merge code khung sườn `Flask-CleanArchitecture`.
    *   [MGMT] Code Review: Kiểm tra các Pull Request (PR) xem code đã đúng tầng (Layer) chưa.
    *   [DOC] Tổng hợp tài liệu SDD (Software Design Document): Cập nhật ERD và Sequence Diagram luồng Login.

### 🛠️ Backend Team (Infrastructure & Logic)
*   **Assignee:** **Lưu Phúc** (Infra), **Quốc Huy** (Domain), **Nguyễn Thuận** (App), **Phúc Cảnh** (Presentation).
*   **Tasks:**
    *   **[BE-01 - Lưu Phúc] Docker Setup:** Viết `Dockerfile` và `docker-compose.yml` để chạy Flask và MySQL 8.0.
    *   **[BE-02 - Lưu Phúc] Database Migration:** Cấu hình Alembic, tạo bảng `users` trong MySQL qua Docker.
    *   **[BE-03 - Quốc Huy] User Entity:** Định nghĩa Class `User` (id, username, password hash, role) trong tầng Domain.
    *   **[BE-04 - Nguyễn Thuận] Auth Use Cases:** Viết logic `LoginUseCase`: Nhận input -> Gọi Repo check user -> Verify Pass -> Tạo JWT Token.
    *   **[BE-05 - Phúc Cảnh] Auth Controller:** Viết API `POST /api/auth/login`, nhận Request Body và trả về JSON chuẩn.

### 💻 Frontend Team (Web & Mobile)
*   **Assignee:** **Ngọc Châu** (Web), **Bruy** (Mobile).
*   **Tasks:**
    *   **[FE-01 - Ngọc Châu] Web Login UI:** Dựng giao diện đăng nhập (NextJS/Tailwind). Cấu hình Axios Interceptor để tự động gắn Token vào Header.
    *   **[MO-01 - Bruy] Mobile Architecture:** Init project Flutter theo cấu trúc sạch (Data/Domain/Presentation).
    *   **[MO-02 - Bruy] Mobile Login:** Dựng màn hình Login, xử lý logic gọi API và lưu Token vào bộ nhớ máy (`flutter_secure_storage`).

---

## 2. Hướng dẫn kỹ thuật (Technical Guidelines)

### A. Cấu trúc Docker (Dành cho Lưu Phúc)
Tạo file `docker-compose.yml` tại thư mục gốc với nội dung sau để cả nhóm cùng dùng chung môi trường DB:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: bizflow_backend
    restart: always
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:root@db/bizflow_db
      - SECRET_KEY=supersecretkey
    volumes:
      - ./backend:/app
    depends_on:
      - db

  db:
    image: mysql:8.0
    container_name: bizflow_db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: bizflow_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### B. Hướng dẫn Refactor Code (Dành cho Dev BE)

1.  **Tầng Domain (`src/domain/entities/user.py`):**
    *   Copy các thuộc tính của User cũ sang đây (id, name, email, password_hash...).
    *   Đây là class thuần Python, không dính dáng đến DB hay Flask.

2.  **Tầng Infrastructure (`src/infrastructure/repositories/user_repository.py`):**
    *   Implement logic truy vấn DB (SQLAlchemy).
    *   Ví dụ hàm `find_by_username(username)`.

3.  **Tầng Application (`src/application/use_cases/auth.py`):**
    *   Đây là nơi chứa logic nghiệp vụ chính (Business Logic).
    *   Sử dụng thư viện `bcrypt` để check pass và `pyjwt` để tạo token.

4.  **Tầng Presentation (`src/presentation/controllers/auth_controller.py`):**
    *   Nơi định nghĩa Route Flask (`@auth_bp.route('/login', methods=['POST'])`).
    *   Chỉ nhận JSON, gọi Use Case, và trả về JSON. Không viết logic `if/else` phức tạp ở đây.

### C. Hướng dẫn Frontend đấu nối
*   **Base URL:** Khi chạy Docker, API sẽ ở `http://localhost:5000`.
*   **Format JSON trả về (Ví dụ):**
    ```json
    {
      "status": "success",
      "data": {
        "access_token": "eyJ0eXAi...",
        "user": {
          "id": 1,
          "username": "admin",
          "role": "owner"
        }
      }
    }
    ```
    *Frontend cần bám sát format này để parse dữ liệu.*

---

## 3. Definition of Done (Tiêu chuẩn hoàn thành)

Sprint 2 chỉ được coi là xong khi thỏa mãn các điều kiện:

1.  [ ] **Docker Run:** Lệnh `docker-compose up` chạy thành công trên máy của cả 7 thành viên mà không lỗi connection.
2.  [ ] **Database:** Bảng `users` đã được tạo trong MySQL và có sẵn 1 user admin (`admin`/`123456`).
3.  [ ] **API Live:** Gọi Postman vào `POST http://localhost:5000/api/auth/login` trả về Token hợp lệ.
4.  [ ] **UI Integration:** Web và App đăng nhập thành công và chuyển hướng vào trang Dashboard/Home.
5.  [ ] **Code Quality:** Code Backend tuân thủ đúng phân chia thư mục của Template Clean Architecture.

---

## 4. Tài liệu cần cập nhật (Documentation)

Sau khi code xong, nhóm cần cập nhật file báo cáo:
*   **SDD (Chapter 4):**
    *   Cập nhật sơ đồ **Deployment Diagram** (thêm hình Docker).
    *   Cập nhật **Sequence Diagram** cho chức năng Login (thể hiện rõ luồng đi qua các tầng Layer).
    *   Cập nhật **ERD** (bảng Users).