# 🏪 BizFlow - Hệ thống Quản lý Cửa hàng Vật liệu Xây dựng

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Hệ thống quản lý bán hàng dành cho cửa hàng vật liệu xây dựng, được xây dựng theo kiến trúc **Clean Architecture** với Flask (Backend) và Next.js (Frontend).

## ✨ Tính năng

### 🔐 Phân quyền 3 cấp

| Role               | Mô tả             | Quyền hạn                                                      |
| ------------------ | ----------------- | -------------------------------------------------------------- |
| **Admin Platform** | Quản trị hệ thống | Quản lý tất cả tài khoản, vô hiệu hóa khi không thanh toán phí |
| **Owner**          | Chủ cửa hàng      | Quản lý nhân viên, sản phẩm, khách hàng, xem báo cáo           |
| **Employee**       | Nhân viên         | Bán hàng (POS), xem sản phẩm, tạo khách hàng mới               |

### 🛒 Quản lý bán hàng (POS)

- Giao diện bán hàng trực quan, dễ sử dụng
- Tìm kiếm sản phẩm nhanh
- Chọn khách hàng hoặc bán lẻ
- Thanh toán: Tiền mặt / Ghi nợ
- Quản lý công nợ khách hàng

### 📦 Quản lý sản phẩm

- Thêm/sửa/xóa sản phẩm
- Phân loại theo danh mục
- Quản lý giá nhập, giá bán
- Theo dõi tồn kho
- Hỗ trợ hình ảnh sản phẩm

### 👥 Quản lý khách hàng

- Thông tin khách hàng
- Lịch sử mua hàng
- Quản lý công nợ
- Ghi nhận thanh toán nợ

### 🤖 Trợ lý AI (Google Gemini)

- Phân tích doanh thu
- Đề xuất sản phẩm bán chạy
- Tư vấn kinh doanh

## 🛠️ Công nghệ sử dụng

### Backend

- **Python 3.9+**
- **Flask 3.0** - Web Framework
- **SQLAlchemy** - ORM
- **MySQL** - Database
- **JWT** - Authentication
- **Bcrypt** - Password Hashing

### Frontend

- **Next.js 15** - React Framework
- **TypeScript** - Type Safety
- **Tailwind CSS** - Styling
- **Shadcn/UI** - UI Components

## 📋 Yêu cầu hệ thống

- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- Git

## 🚀 Cài đặt và Chạy

### 1. Clone repository

```bash
git clone https://github.com/fouzo53/software-engineering-project
cd src
```

### 2. Cài đặt Backend

```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Cài đặt dependencies
pip install -r src/requirements.txt
```

### 3. Tạo Database MySQL

```sql
CREATE DATABASE bizflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Cấu hình môi trường

Chỉnh sửa file `.env`:

```env
# Database - thay đổi password phù hợp
DATABASE_URI=mysql+pymysql://root:your_password@127.0.0.1:3306/bizflow_db

# JWT Secret (thay đổi trong production)
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Google AI API (tùy chọn - cho tính năng AI)
GOOGLE_API_KEY=your-google-api-key
```

### 5. Nạp dữ liệu mẫu

```bash
python seed_vietnamese.py
```

Sau khi chạy, bạn sẽ có:

- **57 sản phẩm** với 5 danh mục
- **20 khách hàng** mẫu
- **30 đơn hàng** lịch sử
- **2 tài khoản**:
  - `admin` / `123456` → Chủ cửa hàng (Owner)
  - `staff` / `123456` → Nhân viên (Employee)

### 6. Chạy Backend

```bash
python run.py
```

Server chạy tại: http://localhost:6868

### 7. Cài đặt và chạy Frontend

```bash
cd frontend

# Cài đặt dependencies
npm install

# Chạy development server
npm run dev
```

Frontend chạy tại: http://localhost:3000

## 📖 Sử dụng

### Đăng nhập

Truy cập http://localhost:3000/login

| Vai trò      | Username | Password |
| ------------ | -------- | -------- |
| Chủ cửa hàng | `admin`  | `123456` |
| Nhân viên    | `staff`  | `123456` |

### Luồng bán hàng

1. Đăng nhập với tài khoản nhân viên hoặc chủ
2. Vào **Bán hàng (POS)**
3. Chọn khách hàng (hoặc để "Khách lẻ")
4. Chọn sản phẩm, điều chỉnh số lượng
5. Chọn phương thức: **Tiền mặt** hoặc **Ghi nợ**
6. Bấm **Thanh toán**

## 📁 Cấu trúc thư mục

```
Flask-CleanArchitecture/
├── src/                          # Backend source
│   ├── api/                      # API Layer
│   │   ├── controllers/          # Route handlers
│   │   ├── schemas/              # Validation schemas
│   │   └── routes.py             # Route registration
│   ├── domain/                   # Domain Layer
│   │   ├── models/               # Domain entities
│   │   └── interfaces/           # Repository interfaces
│   ├── infrastructure/           # Infrastructure Layer
│   │   ├── models/               # SQLAlchemy models
│   │   ├── repositories/         # Repository implementations
│   │   └── databases/            # Database configuration
│   └── services/                 # Application services
├── frontend/                     # Frontend (Next.js)
│   └── src/
│       ├── app/                  # Next.js App Router
│       ├── components/           # React components
│       └── contexts/             # React contexts
├── .env                          # Environment config
├── run.py                        # Backend entry point
└── seed_vietnamese.py            # Sample data seeder
```

## 🔒 Bảo mật

- Mật khẩu được hash bằng **bcrypt**
- Authentication qua **JWT Token**
- Phân quyền 3 cấp (Admin/Owner/Employee)
- Tài khoản có thể bị vô hiệu hóa bởi Admin Platform

## 📝 API Endpoints

| Method | Endpoint             | Mô tả                       |
| ------ | -------------------- | --------------------------- |
| POST   | `/api/auth/login`    | Đăng nhập                   |
| POST   | `/api/auth/register` | Tạo tài khoản (Admin/Owner) |
| GET    | `/api/products`      | Danh sách sản phẩm          |
| POST   | `/api/products`      | Thêm sản phẩm               |
| GET    | `/api/customers`     | Danh sách khách hàng        |
| POST   | `/api/customers`     | Thêm khách hàng             |
| POST   | `/api/orders`        | Tạo đơn hàng                |
| GET    | `/api/categories`    | Danh sách danh mục          |

Swagger UI: http://localhost:6868/docs



⭐ Nếu dự án hữu ích, hãy cho một star nhé!
