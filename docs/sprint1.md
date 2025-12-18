
# 📅 Kế hoạch Sprint 1: Planning & Documentation (1 Tuần)

**Mục tiêu:** Hoàn thiện tài liệu **Capstone Project Document** (Chapter I, II, III, IV sơ bộ) và thiết lập quản lý dự án trên Jira.

---

## 1. Phân chia công việc cho 7 thành viên (Role trong Sprint 1)

Vì chưa code, các thành viên sẽ đóng vai trò là Business Analyst (BA) và System Designer.

| Role            | Số lượng | Thành viên                                  | Nhiệm vụ cụ thể trong Sprint 1                                                     |
| :-------------- | :------: | :------------------------------------------ | :--------------------------------------------------------------------------------- |
| **Leader (PM)** |    1     | Xuân Huy                                    | Viết **Chapter I & II**. Setup Jira/Github. Quản lý tiến độ.                       |
| **BA Team**     |    2     | Quốc Huy, Lưu Phúc, Nguyễn Thuận, Phúc Cảnh | Viết **Chapter III (SRS)**. Vẽ Use Case Diagram. Nghiên cứu Thông tư 88 (Kế toán). |
| **UI/UX Team**  |    2     | Ngọc Châu, Bruy                             | (Là đội FE/Mobile sau này) Vẽ Wireframe (Giao diện nháp) cho Web & Mobile.         |
| **System Arch** |    2     | Xuân Huy, Nguyễn Thuận, Ngọc Châu           | (Là đội BE/AI sau này) Viết **Chapter IV**. Thiết kế Database (ERD) và API List.   |

---

## 2. Cấu trúc Tài liệu cần viết (Dựa trên PDF mẫu)

Nhóm cần tạo 1 file Google Docs (hoặc Word) chung, chia các mục lục y hệt PDF mẫu nhưng nội dung là của BizFlow.

### **I. Project Introduction (Leader viết)**
*Tham khảo PDF trang 6-8*
1.  **Overview:** Tên dự án (BizFlow), Mã lớp, Tên nhóm (4Bees).
2.  **Product Background:** Nêu bối cảnh các hộ kinh doanh VN (Thông tư 88, làm việc thủ công, sổ sách tay).
3.  **Existing Systems:** So sánh với KiotViet, Sapo (Thường quá phức tạp, đắt tiền, không có AI giọng nói tiếng Việt chuyên biệt).
4.  **Business Opportunity:** Giúp hộ kinh doanh chuyển đổi số giá rẻ, tự động hóa kế toán thuế.
5.  **Product Vision:** Trở thành "Kế toán ảo" cho người ít hiểu biết công nghệ.
6.  **Scope & Limitations:**
    *   *Features:* POS, Voice Order, Inventory, Accounting Report.
    *   *Limitations:* AI có thể sai sót cần người xác nhận, cần internet.

### **II. Project Management Plan (Leader viết)**
*Tham khảo PDF trang 9-18*
1.  **Scope & Estimation:** Vẽ bảng WBS cho 8 tuần (Sprint 1 -> Sprint 8).
2.  **Project Deliverables:** Liệt kê những gì sẽ nộp (Source code, User Guide, Báo cáo).
3.  **Responsibility:** Kẻ bảng phân công nhiệm vụ cho 7 người.
4.  **Tools:** ReactJS, Flask, MySQL, GitHub, Jira, Trello/Discord.

### **III. Software Requirement Specification (BA viết)**
*Tham khảo PDF trang 19-24*
1.  **Actors:** Employee, Owner, Admin, System (AI).
2.  **Use Case Diagram:** Vẽ sơ đồ tổng quan (Dùng Draw.io).
3.  **Functional Requirements (Chi tiết):**
    *   *FE-01 (Employee):* Đăng nhập, Tạo đơn hàng, Ghi âm giọng nói.
    *   *FE-02 (Owner):* Quản lý kho, Xem báo cáo doanh thu/công nợ.
    *   *FE-03 (System):* Tự động hạch toán vào sổ cái (Ledger).
4.  **Non-Functional:** Giao diện tiếng Việt đơn giản, Phản hồi < 2s.

### **IV. Software Design Description (System Arch viết)**
*Tham khảo PDF trang 85-92*
1.  **System Architecture:** Vẽ sơ đồ kết nối: ReactJS/Flutter <-> Flask API <-> MySQL.
2.  **Database Design (QUAN TRỌNG NHẤT):** Vẽ ERD (Entity Relationship Diagram).
    *   Các bảng chính: `Users`, `Products`, `Categories`, `Orders`, `OrderItems`, `Customers`, `Transactions` (Cho kế toán).
3.  **UI Design (UI/UX Team):** Chụp ảnh các bản vẽ tay (Wireframe) dán vào đây.
    *   Màn hình Login.
    *   Màn hình POS (Bán hàng).
    *   Màn hình Dashboard (Báo cáo).

---

## 3. Thiết lập trên Jira (Backlog & Sprint 1)

Leader vào Jira tạo Project, sau đó tạo **Sprint 1**. Dưới đây là danh sách các Ticket (Issue) cần tạo:

### 📌 Epic: Project Initiation & Management
- [ ] **[TASK] Setup Collaboration Tools:** Tạo GitHub Repo, Discord Channel, Google Drive Folder. (Assign: Leader)
- [ ] **[TASK] Write Chapter I - Introduction:** Viết tổng quan, bối cảnh, phạm vi dự án. (Assign: Leader)
- [ ] **[TASK] Write Chapter II - Management Plan:** Lên lịch trình 8 tuần, danh sách công cụ. (Assign: Leader)

### 📌 Epic: Requirements & Analysis
- [ ] **[TASK] Research Circular 88 (Thông tư 88):** Liệt kê các quy tắc kế toán cần có (Sổ chi tiết doanh thu, Sổ nợ). (Assign: BA 1)
- [ ] **[TASK] Define Functional Requirements:** Liệt kê chi tiết chức năng cho từng Actor. (Assign: BA 2)
- [ ] **[TASK] Draw Use Case Diagram:** Vẽ sơ đồ Use Case bằng Draw.io. (Assign: BA 1)
- [ ] **[TASK] Write Chapter III - SRS:** Tổng hợp các yêu cầu vào file báo cáo. (Assign: BA Team)

### 📌 Epic: System Design & Database
- [ ] **[TASK] Design Database Schema (ERD):** Thiết kế các bảng MySQL, quan hệ (PK, FK). Chú ý bảng kế toán. (Assign: Sys Arch 1)
- [ ] **[TASK] Define API List (Draft):** Liệt kê các API cần thiết ra Excel (VD: `POST /login`, `GET /products`). (Assign: Sys Arch 2)
- [ ] **[TASK] AI Workflow Design:** Vẽ lưu đồ cách xử lý giọng nói -> Text -> Đơn hàng. (Assign: Sys Arch 2)
- [ ] **[TASK] Write Chapter IV - SDD:** Tổng hợp thiết kế hệ thống và DB vào báo cáo. (Assign: Sys Arch Team)

### 📌 Epic: UI/UX Design
- [ ] **[TASK] Design Mobile Wireframes:** Vẽ nháp màn hình điện thoại (Login, Voice Record, Bill Confirm). (Assign: UI Team 1)
- [ ] **[TASK] Design Web Wireframes:** Vẽ nháp màn hình Admin Web (Dashboard, Product List, Report). (Assign: UI Team 2)
- [ ] **[TASK] Create Mockups:** (Nếu kịp) Chuyển bản vẽ tay sang Figma cơ bản. (Assign: UI Team)

---

## 4. Lịch trình làm việc tuần này (Sample Schedule)

*   **Thứ 2:**
    *   Họp Kick-off (Toàn team).
    *   Leader phân chia công việc trên Jira.
    *   Thống nhất giờ họp Daily (ví dụ 20h tối).
*   **Thứ 3:**
    *   BA nghiên cứu nghiệp vụ.
    *   Sys Arch phác thảo Database.
    *   UI Team vẽ nháp ra giấy.
*   **Thứ 4:**
    *   Họp nhóm Review Database (Cực quan trọng: Cả team phải đồng ý với Database này).
    *   Chốt Use Case Diagram.
*   **Thứ 5:**
    *   Viết nội dung vào file báo cáo chung.
    *   UI Team chốt Flow màn hình.
*   **Thứ 6:**
    *   Review chéo tài liệu.
    *   Chỉnh sửa văn phong tiếng Anh (nếu nộp bằng tiếng Anh).
*   **Thứ 7:**
    *   Tổng hợp file PDF hoàn chỉnh (Version 1.0).
    *   Nộp bài tập/Gửi giảng viên.
    *   Lên kế hoạch Sprint 2 (Bắt đầu code).

---

## 5. Chuẩn bị gì cho tuần sau (Sprint 2 - Coding)?

Để tuần sau bắt tay vào code được ngay, cuối tuần này các bạn cần chốt:
1.  **File SQL:** Một file `database_schema.sql` có sẵn các lệnh `CREATE TABLE`.
2.  **API Contract:** Một file Excel thống nhất Backend sẽ trả về cái gì cho Frontend (JSON format).
3.  **UI Flow:** Hình ảnh giao diện để Frontend cứ thế mà code theo, không phải vừa code vừa nghĩ.

---

### Lời khuyên cho Leader tuần này:
*   File PDF mẫu của FPT rất chi tiết, hãy bám sát mục lục của nó.
*   **Database là xương sống:** Hãy dành nhiều thời gian nhất để tranh luận về Database trong tuần này. Nếu Database sai, tuần sau code sẽ phải đập đi xây lại rất mệt.
*   **Jira Status:** Yêu cầu thành viên kéo thẻ từ `To Do` -> `In Progress` -> `Done` để giảng viên thấy nhóm có hoạt động.
