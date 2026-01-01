**Đánh giá nhanh:**
1.  **Nội dung cốt lõi:** Rất tốt, bám sát đúng đề tài BizFlow, đặc biệt là phần mô tả về Thông tư 88 và AI.
2.  **Vấn đề cần chỉnh sửa:** Cách trình bày **Functional Requirements (Mục 3)** đang bị **"Gộp quá nhiều"**.
    *   Ví dụ: `FE-01` bạn đang nhồi nhét cả: *Login + Tạo đơn + Tìm sản phẩm + Ghi nợ + In hóa đơn + Thông báo*.
    *   **Rủi ro:** Khi chấm đồ án, giảng viên sẽ trừ điểm vì yêu cầu không "Atomic" (đơn nguyên). Làm sao bạn viết Test Case cho FE-01 khi nó bao gồm 6 chức năng khác nhau?
3.  **Phần còn thiếu:** Mục `2.2.2 Use Case Descriptions` đang để trống.

---

# 📝 PHẦN 1: NỘI DUNG CHỈNH SỬA CHAPTER 3 (Copy vào báo cáo)

Thay thế mục **3. Functional Requirements** trong file bằng bảng chi tiết dưới đây. Nó sẽ giúp tài liệu trông dày dặn và chuyên nghiệp hơn.

### 3. Functional Requirements

| ID | Feature Name | Actor | Description |
| :--- | :--- | :--- | :--- |
| **FE-01** | **User Login** | All | Users log into the system using a username/phone number and password. The system verifies credentials and grants access based on roles. |
| **FE-02** | **Product Search & Filtering** | Employee | Employees can quickly search for products by name or category using the search bar or shortcut keys. |
| **FE-03** | **Create At-Counter Order** | Employee | Employees add items to the cart, adjust quantities, select units, and calculate the total amount for walk-in customers. |
| **FE-04** | **Record Customer Debt** | Employee | During checkout, employees can mark the order as "Credit" (Ghi nợ) and assign it to a registered customer. |
| **FE-05** | **Print Sales Receipt** | Employee | The system connects to a printer via Bluetooth/LAN to print sales receipts based on a pre-defined template. |
| **FE-06** | **Voice-to-Order (AI)** | Employee | Users record a voice command (e.g., "5 bags of cement"). The system converts audio to text and generates a draft order. |
| **FE-07** | **Review Draft Order** | Employee | Users review the AI-generated draft order, edit quantities or products if necessary, and confirm to finalize the order. |
| **FE-08** | **Manage Product Catalog** | Owner | Owners can add, update, delete products, set pricing, and define multiple units of measure. |
| **FE-09** | **Manage Inventory** | Owner | Record stock imports, view real-time stock levels, and track inventory transaction history. |
| **FE-10** | **Manage Customers** | Owner | Add new customers, view purchase history, and track total outstanding debt for each customer. |
| **FE-11** | **View Business Reports** | Owner | View dashboards for daily/monthly revenue, best-selling products, and profit estimates. |
| **FE-12** | **Compliance Reporting** | Owner | Automatically generate and export accounting ledgers (Revenue Ledger, Debt Report) strictly following **Circular 88/2021/TT-BTC**. |
| **FE-13** | **Manage Employees** | Owner | Create accounts for employees, reset passwords, and deactivate accounts. |
| **FE-14** | **System Configuration** | Admin | Manage subscription plans, update global report templates, and configure system-wide settings. |

---

# 🚀 PHẦN 2: TASK JIRA (Kế hoạch viết Docs)

Dựa trên nhân sự và tiến độ hiện tại, đây là các task bạn cần tạo trên Jira để hoàn thiện Chapter 3 và chuẩn bị Chapter 4.

**Tên Sprint:** `Documentation & Design`

### 👥 Nhóm BA (Business Analyst)
*   **Thành viên:** Quốc Huy, Lưu Phúc, Phúc Cảnh.
*   **Nhiệm vụ:** Hoàn thiện Chapter 3 và chuẩn bị dữ liệu cho Chapter 4.

| Task ID | Tên Task (Summary) | Assignee | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| **DOC-01** | **Update Functional Req List** | **Quốc Huy** | Thay thế bảng FE cũ bằng bảng FE-01 đến FE-14 (như mẫu trên) vào file báo cáo. |
| **DOC-02** | **Write Use Case Descriptions** | **Lưu Phúc** | Viết mô tả ngắn cho các Use Case chính (Login, Voice Order, Payment, Report). Điền vào mục 2.2.2 đang trống. |
| **DOC-03** | **Design Database Schema (ERD)** | **Nguyễn Thuận** | *Quan trọng:* Vẽ sơ đồ ERD (các bảng Users, Products, Orders, Debt, Ledger). Xuất file ảnh để đưa vào Chapter 4. |
| **DOC-04** | **Define Database Specs** | **Phúc Cảnh** | Kẻ bảng mô tả chi tiết các cột trong Database (Tên cột, kiểu dữ liệu, khóa chính/phụ) dựa trên ERD của Thuận. |

### 🎨 Nhóm UI/UX & Mobile
*   **Thành viên:** Ngọc Châu, Bruy.
*   **Nhiệm vụ:** Chuẩn bị hình ảnh giao diện cho Chapter 4.

| Task ID | Tên Task (Summary) | Assignee | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| **DOC-05** | **Design Mobile Wireframes** | **Bruy** | Vẽ/Chụp màn hình App Mobile: Login, Trang bán hàng (POS), Màn hình Micro (Voice). Đưa vào Chapter 4. |
| **DOC-06** | **Design Web Wireframes** | **Ngọc Châu** | Vẽ/Chụp màn hình Web: Dashboard doanh thu, Danh sách sản phẩm, Báo cáo sổ sách. Đưa vào Chapter 4. |

### 👑 Nhóm Leader
*   **Thành viên:** Xuân Huy.

| Task ID | Tên Task (Summary) | Assignee | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| **DOC-07** | **Merge & Review Document** | **Xuân Huy** | Nhận nội dung từ các thành viên, ghép vào file Docs tổng. Chỉnh sửa font chữ, mục lục. Xuất file PDF. |
| **DOC-08** | **Create System Arch Diagram** | **Xuân Huy** | Vẽ sơ đồ kiến trúc hệ thống (Mobile/Web <-> API <-> DB/AI) để đưa vào đầu Chapter 4. |

---

### 💡 Hướng dẫn thêm cho mục "2.2.2 Use Case Descriptions" (Đang trống)

Đây là mẫu cho bạn **Lưu Phúc** để làm nhanh task **DOC-02**:

**Mẫu viết Use Case Description:**
*   **UC-01: Create Order via Voice**
    *   **Actor:** Employee
    *   **Pre-condition:** Employee is logged in and on the POS screen.
    *   **Main Flow:**
        1.  Employee taps the "Microphone" icon.
        2.  Employee speaks the order (e.g., "Bán 2 bao xi măng").
        3.  System processes voice to text and identifies product/quantity.
        4.  System displays a Draft Order.
        5.  Employee reviews and clicks "Confirm".
        6.  System saves order and updates inventory.
    *   **Post-condition:** Order is created, Revenue Ledger is updated.

Chỉ cần viết khoảng 3-4 Use Case chính như vậy là đủ đẹp cho Chapter 3. (Tùy mục đích, có gì sẽ chỉnh sửa/bổ sung lại)
