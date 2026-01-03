### CHƯƠNG IV: SOFTWARE DESIGN DESCRIPTION (SDD)
*Tập trung vào thiết kế thực tế của BizFlow, lược bỏ các phần lý thuyết rườm rà.*

| Thành viên | Task ID | Tên Task & Vị trí trong Template | Mô tả chi tiết nội dung cần viết |
| :--- | :--- | :--- | :--- |
| **Lưu Võ Thiên Phúc** | **BF-4.1** | **IV.1: System Design** | Vẽ và giải thích sơ đồ **System Architecture** (Clean Architecture). Mô tả các tầng: Presentation (NextJS/Flutter), Application (Flask/Python), Domain (Logic nghiệp vụ), Infrastructure (DB/Redis). |
| **Njan Bruy** | **BF-4.2** | **IV.2: Database Design** | Vẽ sơ đồ **ERD** cuối cùng của dự án. Viết bảng mô tả (Data Dictionary) cho các bảng chính: `Product`, `Order`, `Debt`, `Ledger`, `AI_Prompt`. (Chỉ làm bảng chính). |
| **Lê Hà Quốc Huy** | **BF-4.3** | **IV.3: Detailed Design** | Vẽ **Sequence Diagram** cho 2 luồng quan trọng: 1. AI nhận diện voice -> tạo đơn hàng nháp. 2. Chốt đơn hàng -> Tự động ghi sổ (theo Thông tư 88). |

---

### CHƯƠNG V: SOFTWARE TESTING DOCUMENTATION
*Chứng minh dự án BizFlow nhỏ nhưng chạy cực kỳ ổn định và chính xác.*

| Thành viên | Task ID | Tên Task & Vị trí trong Template | Mô tả chi tiết nội dung cần viết |
| :--- | :--- | :--- | :--- |
| **Lê Ngọc Châu** | **BF-5.1** | **V.1 & V.3: Test Strategy & Plan** | Viết phạm vi test (tập trung tính năng AI và báo cáo thuế). Lập danh sách **Test Cases** cho luồng POS và quản lý nợ. (Làm bảng ngắn gọn). |
| **Nguyễn Phúc Cảnh** | **BF-5.2** | **V.5: Test Reports** | Tổng hợp kết quả test thực tế. Viết kết quả **UAT** (Test với người dùng): Thử đọc 10 câu lệnh tiếng Việt vào app, thống kê bao nhiêu câu AI hiểu đúng, bao nhiêu câu sai. |

---

### CHƯƠNG VI: RELEASE PACKAGE & USER GUIDES
*Đóng gói dự án và hướng dẫn sử dụng bằng hình ảnh.*

| Thành viên | Task ID | Tên Task & Vị trí trong Template | Mô tả chi tiết nội dung cần viết |
| :--- | :--- | :--- | :--- |
| **Lê Hà Quốc Huy** | **BF-6.1** | **VI.2: Installation Guides** | Viết hướng dẫn cài đặt Backend Python, AI Service và Database. Liệt kê các lệnh `pip install`, `docker-compose up`. |
| **Nguyễn Phúc Cảnh** | **BF-6.2** | **VI.2: Installation Guides** | Viết hướng dẫn cài đặt Web (Next.js) và Mobile (Flutter). Hướng dẫn build file `.apk` cho Android để chủ hộ sử dụng. |
| **Lưu Võ Thiên Phúc** | **BF-6.3** | **VI.3: User Manual (Mobile)** | Chụp ảnh màn hình App Mobile. Viết hướng dẫn: Đăng nhập -> Ấn nút ghi âm -> Kiểm tra đơn hàng -> In biên lai. |
| **Lê Ngọc Châu** | **BF-6.4** | **VI.3: User Manual (Web)** | Chụp ảnh Dashboard trên Web. Viết hướng dẫn: Quản lý kho -> Xem nợ khách hàng -> Xuất báo cáo thuế Thông tư 88 ra file PDF. |

---

### TỔNG HỢP VAI TRÒ CỦA PM

| Task ID | Công việc chính | Lưu ý thực hiện |
| :--- | :--- | :--- |
| **BF-PM-QC** | **Review & Format** | Đọc lại nội dung các thành viên gửi. Đảm bảo thuật ngữ đồng nhất (Ví dụ: Không được chỗ gọi là "Draft Order", chỗ gọi là "Đơn tạm"). |
| **BF-PM-MG** | **Merge to Master Doc** | Gom tất cả các phần vào file Word/LaTeX chính. Kiểm tra mục lục, đánh số hình vẽ (Figure 4.1, 5.1...) và danh mục bảng biểu. |
| **BF-PM-SUB** | **Final Submission** | Xuất file PDF cuối cùng, kiểm tra lại dung lượng file và nộp bài đúng hạn. |

---

### 💡 Gợi ý lược bỏ để làm nhanh:
1.  **Chương IV:** Không cần vẽ Class Diagram cho mọi lớp, chỉ vẽ cho các Entity chính của Database.
2.  **Chương V:** Lược bỏ phần "Test Environment" chi tiết (chỉ cần nêu: Test trên iPhone 13/Laptop Dell). Không viết hàng trăm test case, chỉ viết khoảng 15-20 case đại diện cho các tính năng cốt lõi.
3.  **Chương VI:** Phần "Deliverable Package" chỉ cần liệt kê danh sách file nộp (Source code, Docs, Slide).