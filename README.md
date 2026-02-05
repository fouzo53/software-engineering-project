# 🏪 BizFlow - Hệ thống Quản lý Cửa hàng Vật liệu Xây dựng

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Hệ thống quản lý bán hàng dành cho cửa hàng vật liệu xây dựng, được xây dựng theo kiến trúc **Clean Architecture** với Flask (Backend) và Next.js (Frontend). Dự án tích hợp AI (Gemini) để hỗ trợ phân tích và tạo đơn hàng bằng giọng nói/văn bản.

## ✨ Tính năng chính

- **Giao diện POS hiện đại**: Tối ưu cho thao tác nhanh, hỗ trợ cả máy tính và máy tính bảng.
- **Phân quyền 3 cấp**: Admin (Hệ thống) / Owner (Chủ shop) / Employee (Nhân viên).
- **Trợ lý AI (Gemini)**: 
  - Tạo đơn hàng tự động từ văn bản hoặc giọng nói.
  - Phân tích doanh thu và đề xuất kinh doanh.
- **Quản lý công nợ**: Theo dõi nợ khách hàng, ghi sổ tự động theo thông tư 88/2021/TT-BTC.
- **Báo cáo tài chính**: Sổ doanh thu (S1), Sổ chi tiết vật liệu (S2), Sổ quỹ tiền mặt (S4/S6).

## 🛠️ Công nghệ sử dụng

- **Backend**: Python 3.9+, Flask, SQLAlchemy (MySQL), Marshmallow, JWT, Google Generative AI, OpenAI Whisper.
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Shadcn/UI, Lucide Icons.
- **Infrastructure**: MySQL, Redis, Docker.

## 🚀 Hướng dẫn cài đặt nhanh

### 1. Chuẩn bị môi trường
Yêu cầu: Git, Python 3.9+, Node.js 18+, MySQL 8.0+.

```bash
git clone https://github.com/fouzo53/software-engineering-project
cd software-engineering-project
```

### 2. Cấu hình biến môi trường
Dự án sử dụng file `.env` để quản lý cấu hình. Bạn cần tạo các file này từ file ví dụ:

**Backend:**
```bash
cp .env.example .env
# Sau đó chỉnh sửa .env để cập nhật DATABASE_URI và GOOGLE_API_KEY
```

**Frontend:**
```bash
cd frontend
cp .env.example .env.local
cd ..
```

### 3. Cài đặt Backend & Nạp dữ liệu
```bash
# Tạo và kích hoạt Virtual Env
python -m venv .venv
source .venv/bin/activate  # Hoặc .venv\Scripts\activate trên Windows

# Cài đặt thư viện
pip install -r requirements.txt

# Tạo database MySQL (tên: bizflow_db) và chạy script nạp dữ liệu mẫu
python src/scripts/seed_vietnamese.py
```

### 4. Chạy ứng dụng

**Chạy Backend (Cổng 6868):**
```bash
python run.py
```

**Chạy Frontend (Cổng 3000):**
```bash
cd frontend
bun install
bun dev
```

## 🐳 Chạy bằng Docker (Khuyên dùng)
Nếu bạn có Docker, bạn có thể khởi động cơ sở dữ liệu và các dịch vụ hỗ trợ nhanh chóng:

```bash
docker-compose up -d
```
Lệnh này sẽ khởi chạy MySQL (cổng 3306), Redis (cổng 6379) và phpMyAdmin (cổng 8080).

## 🔐 Tài khoản dùng thử

| Vai trò | Username | Password |
| :--- | :--- | :--- |
| **Chủ cửa hàng (Owner)** | `owner` | `123456` |
| **Quản trị viên (Admin)** | `admin` | `123456` |
| **Nhân viên (Staff)** | `staff` | `123456` |