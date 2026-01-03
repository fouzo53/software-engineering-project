### 1. Tổng quan logic thiết kế
Dự án **BizFlow** sử dụng cấu trúc **Multi-tenancy** (Đa hộ kinh doanh). Nghĩa là một hệ thống có thể phục vụ nhiều cửa hàng khác nhau cùng lúc. Do đó, hầu hết các bảng đều có khóa ngoại `store_id` để phân tách dữ liệu của hộ kinh doanh A và hộ kinh doanh B.

---

### 2. Chi tiết các cụm thực thể (Entity Groups)

#### Cụm A: Quản lý Tổ chức & Người dùng (The Foundation)
*   **stores:** Lưu thông tin hộ kinh doanh (Tên cửa hàng, địa chỉ, hotline). Đây là "cha" của mọi dữ liệu khác.
*   **users:** Danh sách người dùng hệ thống.
*   **store_users:** Bảng trung gian để phân quyền. Một `user` có thể làm `Owner` (Chủ) hoặc `Staff` (Nhân viên) của một `store`.
    *   *Tại sao cần bảng này?* Để hỗ trợ chủ hộ có thể thuê nhiều nhân viên, hoặc một người có thể sở hữu nhiều cửa hàng.

#### Cụm B: Danh mục Sản phẩm & Kho hàng (Product & Inventory)
*   **categories:** Phân loại sản phẩm (Ví dụ: Nhóm Xi măng, Nhóm Sắt thép, Nhóm Đồ điện).
*   **products:** Thông tin chung của sản phẩm.
*   **product_units (Quan trọng):** Một sản phẩm có thể có nhiều đơn vị tính (Ví dụ: Sắt bán theo "Cây" hoặc theo "Tạ"). 
    *   `conversion_factor`: Tỷ lệ quy đổi (Ví dụ: 1 bao xi măng = 50kg).
    *   `current_stock`: Số lượng tồn kho thực tế của đơn vị đó.
*   **inventory_imports & inventory_import_items:** Lưu lại lịch sử khi chủ hộ nhập hàng từ nhà cung cấp. 
    *   *Ý nghĩa:* Giúp tự động hóa **Sổ S2** (Sổ chi tiết vật liệu, dụng cụ, sản phẩm, hàng hóa) theo Thông tư 88.

#### Cụm C: Bán hàng & Giao dịch (The Sales Flow)
*   **orders:** Lưu thông tin tổng quát của một hóa đơn (Tổng tiền, trạng thái, ngày tạo).
    *   `payment_method`: Lưu 'cash' (Tiền mặt) hoặc 'bank_transfer' (Chuyển khoản). Đây là dữ liệu nguồn để tự động xuất **Sổ S6** (Sổ quỹ tiền mặt) và **Sổ S7** (Sổ tiền gửi ngân hàng).
*   **order_items:** Chi tiết từng món hàng trong đơn (Mua loại gì, số lượng bao nhiêu, giá bán lúc đó).
*   **ai_draft_orders (Linh hồn của BizFlow):** Khi nhân viên nói "Lấy cho ông Ba 5 bao xi măng", AI sẽ xử lý và lưu vào đây dưới dạng **"Đơn hàng nháp"**. 
    *   Nhân viên chỉ cần bấm "Xác nhận", dữ liệu từ đây sẽ được copy sang bảng `orders` chính thức.

#### Cụm D: Khách hàng & Công nợ (CRM & Debt)
*   **customers:** Danh sách khách quen. 
    *   `current_debt`: Con số tổng nợ hiện tại của khách đó.
*   **debt_transaction_logs:** Nhật ký biến động nợ.
    *   *Tại sao cần?* Truy xuất lịch sử: Ngày X khách mua nợ 5 triệu (tăng), Ngày Y khách trả 2 triệu (giảm). 
    *   *Ý nghĩa:* Giúp tự động hóa **Sổ S1** (Sổ chi tiết doanh thu bán hàng hóa, dịch vụ) phần theo dõi nợ.

---

### 3. Cách dữ liệu "chảy" trong hệ thống (Dành cho Dev & BA)

1.  **Luồng Bán hàng AI:** `Voice` -> `ai_draft_orders` -> `Nhân viên bấm Confirm` -> tạo `orders` & `order_items` -> trừ `current_stock` trong `product_units`.
2.  **Luồng Công nợ:** Nếu khách mua nợ, hệ thống tạo một bản ghi trong `debt_transaction_logs` -> cộng dồn vào `current_debt` của `customers`.
3.  **Luồng Kế toán (Thông tư 88):**
    *   **Sổ S1 (Doanh thu):** Lấy từ `orders`.
    *   **Sổ S2 (Kho):** Lấy từ `inventory_imports` và `order_items`.
    *   **Sổ S6 & S7 (Tiền mặt/Ngân hàng):** Lấy từ `orders` dựa trên `payment_method`.

---

### 4. Gợi ý cho các thành viên viết Task:

*   **Njan Bruy (Database Design):** Khi viết mô tả, hãy nhấn mạnh tính **nhất quán dữ liệu**. Ví dụ: Dùng `DECIMAL` cho tiền tệ để tránh sai số dấu phẩy động của `FLOAT`.
*   **Lê Hà Quốc Huy (Detailed Design):** Khi vẽ Sequence Diagram, hãy bám sát luồng: `AI Service -> ai_draft_orders -> Database`.
*   **Lê Ngọc Châu (Testing):** Test case quan trọng nhất là: "Khi xóa một `order`, số lượng tồn kho trong `product_units` có được cộng trả lại không?" (Integrity Test).
*   **Phúc & Cảnh (User Manual):** Hãy chụp ảnh màn hình nơi hiển thị "Phương thức thanh toán" để chứng minh App giúp chủ hộ làm báo cáo thuế dễ dàng.
