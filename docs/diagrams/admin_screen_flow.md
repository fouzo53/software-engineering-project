# Luồng Màn Hình Admin (BizFlow - Simple Version)

## Mục tiêu
Để tối ưu cho một **dự án nhỏ như BizFlow**, luồng màn hình (Screen Flow) dành cho **vai trò Admin** nên được **tinh gọn**, chỉ tập trung vào **các chức năng quản trị hệ thống cốt lõi**, thay vì các nghiệp vụ bán hàng của nhân viên hay chủ hộ.

***

## Sơ đồ luồng màn hình

### 1. **Màn hình Đăng nhập (Login Page)**
- **Hành động:** Admin nhập tài khoản và mật khẩu hệ thống.  
- **Kết quả:** Hệ thống xác thực quyền "Admin" và chuyển hướng vào **Dashboard**.

### 2. **Màn hình Tổng quan (Admin Dashboard)**
- **Hiển thị:**  
  - Tổng số hộ kinh doanh.  
  - Tổng doanh thu nền tảng.  
  - Trạng thái hệ thống.  
- **Menu điều hướng:**  
  - Quản lý tài khoản.  
  - Cấu hình hệ thống.

### 3. **Màn hình Quản lý hộ kinh doanh (User Management - Owner List)**
- **Chức năng:**  
  - Hiển thị danh sách các chủ hộ kinh doanh đã đăng ký.  
  - Hành động: **Kích hoạt (Activate)** hoặc **Vô hiệu hóa (Deactivate)** tài khoản.

### 4. **Màn hình Cấu hình & Gói dịch vụ (System Configuration)**
- **Chức năng:**  
  - Chỉnh sửa giá các gói dịch vụ (Basic, Pro).  
  - Cập nhật các mẫu báo cáo theo **Thông tư 88/2021/TT-BTC** khi có thay đổi từ nhà nước.

***

## Mô tả chi tiết luồng (Step-by-Step)

| **Từ màn hình** | **Hành động của Admin** | **Đến màn hình / Kết quả** |
|------------------|---------------------------|-----------------------------|
| Login Page | Nhập Credential của Admin | Admin Dashboard |
| Admin Dashboard | Chọn "Quản lý hộ kinh doanh" | Owner Account List (Xem danh sách) |
| Owner Account List | Nhấn nút "On/Off" trạng thái tài khoản | Cập nhật trạng thái trực tiếp trên danh sách |
| Admin Dashboard | Chọn "Cấu hình hệ thống" | Configuration Screen |
| Configuration Screen | Nhập giá mới hoặc upload mẫu file .pdf/.xlsx | Lưu cấu hình hệ thống |

***

## Tại sao luồng này phù hợp với dự án nhỏ?

- **Tập trung vào "Cổng" (Gatekeeper):**  
  Admin trong dự án nhỏ thường chỉ đóng vai trò duyệt người dùng và cài đặt các tham số chung cho AI hoặc báo cáo thuế.

- **Lược bỏ chi tiết không cần thiết:**  
  Không cần các màn hình con như **"Xem chi tiết người dùng"** hay **"Import User"** nếu số lượng hộ kinh doanh chưa lớn.

- **Dễ triển khai:**  
  Luồng này bám sát **chức năng FE-14 (System Configuration)** trong danh sách yêu cầu chức năng của BizFlow.

***

## Ví dụ

Luồng Admin này giống như **bảng điều khiển của một người quản lý khu chợ**:
1. Cho phép gian hàng nào được mở cửa → **Quản lý tài khoản**.  
2. Quy định mức phí thuê chỗ và mẫu biên lai chung → **Cấu hình hệ thống**.
