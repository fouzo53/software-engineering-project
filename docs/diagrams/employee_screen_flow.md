## Luồng màn hình Employee (BizFlow - Simple Version)

### 1. Màn hình Đăng nhập (Login Page)
- Nhân viên nhập số điện thoại/tên đăng nhập và mật khẩu.  
- Hệ thống xác thực vai trò **Employee** và chuyển hướng vào **POS Screen** (màn hình bán hàng chính).

***

### 2. Màn hình Bán hàng chính (POS Screen)
- **Tìm kiếm sản phẩm**: Ô tìm kiếm nhanh theo tên, mã hoặc danh mục, kết quả cho phép thêm nhanh vào giỏ hàng.  
- **Giỏ hàng (Cart)**: Danh sách mặt hàng đã chọn, có thể chỉnh số lượng và đơn vị tính.  
- **Nút Micro (AI Voice-to-Order)**: Kích hoạt chế độ tạo đơn bằng giọng nói.

***

### 3. Màn hình Tạo đơn bằng Giọng nói (AI Voice-to-Order)
- **Ghi âm**: Nhân viên nhấn/nhấn giữ nút Micro và đọc yêu cầu, ví dụ: “Lấy 5 bao xi măng cho ông Ba, ghi nợ”.  
- **Xử lý AI**: Hệ thống chuyển giọng nói thành văn bản, nhận diện sản phẩm, số lượng, loại giao dịch (ghi nợ/thanh toán ngay).  
- **Đơn hàng nháp (Draft Order)**: Hiển thị kết quả nhận diện để nhân viên xem lại, chỉnh sửa nếu cần trước khi xác nhận.

***

### 4. Màn hình Thanh toán & Ghi nợ (Checkout & Debt)
- **Chọn khách hàng**: Tìm kiếm khách hàng thân thiết trong hệ thống hoặc chọn khách lẻ.  
- **Ghi nợ**: Tùy chọn đánh dấu “Ghi nợ” nếu khách chưa thanh toán ngay; nếu không sẽ ghi nhận thanh toán đủ.  
- **Xác nhận**: Hoàn tất đơn hàng, tự động hạch toán vào sổ cái hệ thống.

***

### 5. Màn hình In hóa đơn (Print Receipt)
- Hiển thị thông tin đơn hàng cuối cùng: danh sách hàng, tổng tiền, trạng thái thanh toán/ghi nợ.  
- Nút “In hóa đơn” để in qua máy in Bluetooth hoặc LAN.

***

### 6. Bảng Step-by-Step luồng thao tác

| Từ màn hình      | Hành động của Nhân viên                          | Đến màn hình / Kết quả                         |
|------------------|--------------------------------------------------|-----------------------------------------------|
| Login Page       | Đăng nhập tài khoản Employee                     | POS Screen (màn hình bán hàng chính)         |
| POS Screen       | Nhập tên sản phẩm vào ô tìm kiếm                 | Thêm sản phẩm từ danh sách gợi ý vào giỏ      |
| POS Screen       | Nhấn nút Micro và đọc đơn hàng                   | Màn hình Đơn hàng nháp (AI tạo)              |
| Đơn nháp         | Kiểm tra thông tin, chỉnh sửa nếu cần và “Xác nhận” | Màn hình Thanh toán                          |
| Thanh toán       | Chọn khách hàng và chọn “Ghi nợ” hoặc thanh toán ngay | Xác nhận thành công & Cập nhật công nợ/sổ cái |
| Xác nhận         | Nhấn nút “In hóa đơn”                            | Xuất biên lai từ máy in                      | 

***

### 7. Các điểm lưu ý cho dự án nhỏ

- **Giao diện đơn giản (Usability)**: Tối thiểu số lần chạm, nút lớn, quy trình tuyến tính để phù hợp người dùng có kỹ năng số thấp.
- **Human-in-the-loop**: Mọi đơn hàng do AI tạo đều phải qua bước “Đơn nháp” để nhân viên xem lại và xác nhận, giảm rủi ro sai sót.
- **Thông báo thời gian thực**: Nhân viên nhận thông báo khi hệ thống/Chatbot tạo một đơn nháp từ xa (ví dụ từ Zalo), có thể mở nhanh đơn nháp đó trên POS và tiếp tục bước xác nhận/thu tiền.

***

### 8. Ẩn dụ nghiệp vụ

Luồng của nhân viên bán hàng giống như **một người bồi bàn thông minh**:  
- Có thể nhập món bằng tay hoặc để “máy nghe – máy hiểu – máy lên đơn” từ giọng nói.  
- Cuối cùng chỉ cần hỏi khách “Trả tiền ngay hay ký sổ?” rồi in hóa đơn.