## AI Draft Order API Contract (Backend ↔ AI Service)

### 1. Context

**BizFlow** hỗ trợ nhân viên bán hàng tạo **đơn nháp (AI Draft Order)** từ câu lệnh tiếng Việt (voice/text).  
Luồng tổng quát (tham chiếu SRS/SDD & UAT trong `bizflow.pdf`):

- Nhân viên nhập câu lệnh (voice hoặc text), ví dụ:  
  *"Lấy cho anh Ba 5 bao xi măng, ghi nợ"*
- Hệ thống chuyển voice → text (STT) nếu cần.
- Backend gọi **AI service** để:
  - Nhận diện sản phẩm, số lượng, đơn vị.
  - Nhận diện khách hàng.
  - Nhận diện hình thức thanh toán (tiền mặt/nợ).
- AI trả về kết quả parse dưới dạng **draft order** cùng thông tin độ tin cậy & cảnh báo.
- Backend lưu draft vào DB (bảng `AI_draft_order` hoặc `Orders` với status `draft`).
- Web / Mobile hiển thị draft để người dùng kiểm tra & xác nhận.

Mục tiêu tài liệu này:

- Chuẩn hóa **contract REST** giữa **Backend** và **AI service** cho tính năng AI Draft Order.
- Làm cơ sở để backend, AI, mobile & web implement độc lập nhưng tương thích.

---

### 2. Sequence Flow (High Level)

1. **Mobile/Web** gửi câu lệnh (voice hoặc text) đến **Backend**.
2. Backend:
   - Chuẩn hóa input (business_id, employee_id, channel, …).
   - Gửi request sang **AI service**: `/ai/v1/draft-orders/parse`.
3. **AI service**:
   - (Nếu `input_type = "audio"`) chạy STT để có transcript.
   - Dùng LLM + RAG để map câu lệnh ↔ sản phẩm, khách hàng, hình thức thanh toán.
   - Trả về JSON draft order + thông tin độ tin cậy, issues.
4. Backend:
   - Lưu raw request/response AI vào DB (phục vụ phân tích sau).
   - Tạo bản ghi **AI Draft Order** (status `draft` hoặc `needs_review`).
5. **Frontend (Web/Mobile)**:
   - Gọi backend để lấy danh sách draft orders.
   - Cho người dùng confirm / chỉnh sửa / huỷ.

---

### 3. API Contract: Backend → AI Service

#### 3.1. Endpoint tổng quan

- **Method**: `POST`
- **URL (AI service)**: `/ai/v1/draft-orders/parse`
- **Headers**:
  - `Content-Type: application/json`
  - `X-Internal-Token: <INTERNAL_API_TOKEN>` (hoặc cơ chế auth nội bộ khác)

#### 3.2. Request Schema

```json
{
  "request_id": "b4d9f6e2-3a11-4d7b-8a5f-1c0b5d6f9a01",
  "business_id": 123,
  "input_type": "text",
  "locale": "vi-VN",
  "channel": "mobile_voice",
  "user_context": {
    "employee_id": 456,
    "store_id": 123,
    "source": "phone"
  },
  "input_text": "Lấy cho anh Ba 5 bao xi măng, ghi nợ",
  "audio_url": null,
  "constraints": {
    "max_candidates": 3,
    "min_confidence": 0.6
  }
}
```

**Mô tả trường chính:**

- **`request_id`** *(string, optional nhưng khuyến khích)*  
  ID duy nhất để trace log giữa backend ↔ AI.
- **`business_id`** *(number, required)*  
  ID cửa hàng, dùng để AI tra cứu đúng catalog sản phẩm & khách hàng.
- **`input_type`** *(string, required)*  
  - `"text"`: chỉ gửi text.
  - `"audio"`: gửi link audio, AI sẽ tự STT (hoặc dùng `input_text` nếu backend đã STT trước).
- **`locale`** *(string, optional, default `"vi-VN"`)*  
  Locale ngôn ngữ, hiện tại chủ yếu `vi-VN`.
- **`channel`** *(string, optional)*  
  Kênh tạo đơn: `"mobile_voice"`, `"mobile_text"`, `"web_text"`, `"phone"`, …
- **`user_context`** *(object, optional)*  
  - `employee_id`: ID nhân viên.
  - `store_id`: ID cửa hàng/chi nhánh (nếu đa chi nhánh).
  - `source`: mô tả nguồn, ví dụ `"zalo"`, `"phone"`, `"counter"`.
- **`input_text`** *(string, optional)*  
  Câu lệnh tiếng Việt sau khi STT (nếu có).  
  - Bắt buộc nếu `input_type = "text"`.
  - Có thể null nếu `input_type = "audio"` và AI tự STT.
- **`audio_url`** *(string, optional)*  
  URL file audio (backend đã upload lên storage nội bộ hoặc S3, MinIO, …).  
  - Bắt buộc nếu `input_type = "audio"` (trừ khi team thống nhất ngược lại).
- **`constraints`** *(object, optional)*  
  - `max_candidates` *(number)*: tối đa số candidate sản phẩm/khách muốn trả về (nếu AI hỗ trợ).
  - `min_confidence` *(number 0–1)*: ngưỡng độ tin cậy tối thiểu.

#### 3.3. Response Schema – Thành công

```json
{
  "request_id": "b4d9f6e2-3a11-4d7b-8a5f-1c0b5d6f9a01",
  "status": "ok",
  "transcript": {
    "original_text": "Lấy cho anh Ba 5 bao xi măng, ghi nợ",
    "normalized_text": "Lấy cho Anh Ba 5 bao xi măng, ghi nợ",
    "source": "stt"
  },
  "draft_order": {
    "customer": {
      "match_type": "exact",
      "customer_id": "c1",
      "name": "Anh Ba",
      "confidence": 0.92
    },
    "items": [
      {
        "product": {
          "match_type": "exact",
          "product_id": "p1",
          "name": "Xi măng Portland PCB40",
          "sku": "XM-PCB40",
          "confidence": 0.88
        },
        "quantity": 5,
        "unit": "bao",
        "unit_confidence": 0.95,
        "notes": null
      }
    ],
    "payment": {
      "type": "debt",
      "confidence": 0.9
    },
    "meta": {
      "source": "ai",
      "channel": "mobile_voice",
      "suggested_status": "draft"
    }
  },
  "confidence": 0.87,
  "issues": [],
  "warnings": []
}
```

**Giải thích:**

- **`status`** *(string)*:
  - `"ok"`: Có thể tạo draft order, thông tin tương đối đầy đủ.
  - `"needs_review"`: Có vấn đề (thiếu thông tin / độ tin cậy thấp), nhưng vẫn trả draft để người dùng hiệu chỉnh.
  - `"error"`: Lỗi nghiêm trọng, không thể parse.
- **`transcript`**:
  - `original_text`: Text ban đầu (sau STT hoặc input gốc).
  - `normalized_text`: Text đã chuẩn hóa (chữ hoa/thường, dấu, …) phục vụ hiển thị/log.
  - `source`: `"stt"` | `"user_input"` | `"unknown"`.
- **`draft_order`**:
  - `customer`:
    - `match_type`: `"exact"` | `"fuzzy"` | `"none"`.
    - `customer_id`: ID khách trong DB (nullable).
    - `name`: Tên khách mà AI hiểu.
    - `confidence`: Độ tin cậy 0–1.
  - `items[]`:
    - `product`:
      - `match_type`: `"exact"` | `"fuzzy"` | `"ambiguous"`.
      - `product_id`: ID sản phẩm trong DB (nullable nếu không chắc).
      - `name`, `sku`, `confidence`.
    - `quantity`: Số lượng (number).
    - `unit`: Đơn vị (string, ví dụ `"bao"`, `"m³"`, `"viên"`).
    - `unit_confidence`: Độ tin cậy đơn vị 0–1.
    - `notes`: Ghi chú thêm nếu cần (ví dụ: “unit inferred from context”).
  - `payment`:
    - `type`: `"cash"` | `"debt"` | `"unknown"`.
    - `confidence`: 0–1.
  - `meta`:
    - `source`: `"ai"`.
    - `channel`: copy từ request.
    - `suggested_status`: `"draft"` | `"needs_review"`.
- **`confidence`**: Độ tin cậy tổng thể cho toàn bộ draft.
- **`issues`**:
  - Danh sách các vấn đề AI phát hiện, dùng cho UI highlight.
- **`warnings`**:
  - Chuỗi cảnh báo hiển thị cho người dùng cuối hoặc log.

#### 3.4. Response – Case cần review (ví dụ từ UAT)

Ví dụ mệnh lệnh: *"Lấy 20 viên gạch đỏ"* (thiếu khách & payment type), tương tự các case lỗi được ghi trong mục UAT 5.3 của `bizflow.pdf`.

```json
{
  "request_id": "....",
  "status": "needs_review",
  "transcript": {
    "original_text": "Lấy 20 viên gạch đỏ",
    "normalized_text": "Lấy 20 viên gạch đỏ",
    "source": "stt"
  },
  "draft_order": {
    "customer": null,
    "items": [
      {
        "product": {
          "match_type": "fuzzy",
          "product_id": "p3",
          "name": "Gạch ống đỏ 4x8x19",
          "sku": "GOD-4x8x19",
          "confidence": 0.7
        },
        "quantity": 20,
        "unit": "viên",
        "unit_confidence": 0.9,
        "notes": "Customer not identified"
      }
    ],
    "payment": {
      "type": "unknown",
      "confidence": 0.0
    },
    "meta": {
      "source": "ai",
      "channel": "mobile_voice",
      "suggested_status": "needs_review"
    }
  },
  "confidence": 0.65,
  "issues": [
    {
      "code": "MISSING_CUSTOMER",
      "message": "Customer could not be confidently identified.",
      "severity": "warning"
    },
    {
      "code": "PAYMENT_TYPE_UNKNOWN",
      "message": "Payment type not clearly stated.",
      "severity": "warning"
    }
  ],
  "warnings": [
    "User should review customer and payment type before confirming."
  ]
}
```

#### 3.5. Error Response Schema

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Input text is empty.",
    "details": {
      "field": "input_text"
    }
  }
}
```

Gợi ý các `code`:

- `INVALID_INPUT`
- `LOW_CONFIDENCE`
- `INTERNAL_ERROR`
- `UNSUPPORTED_LOCALE`

---

### 4. Trạng thái & Mapping với Backend

#### 4.1. Trạng thái từ AI Response

- `status = "ok"`  
  → Backend có thể tạo draft order với trạng thái `draft` (vẫn cho chỉnh sửa).
- `status = "needs_review"`  
  → Backend tạo draft order với trạng thái `needs_review`, UI phải highlight để người dùng kiểm tra kỹ.
- `status = "error"`  
  → Backend không tạo draft; trả lỗi cho frontend (hiện thông báo “AI không hiểu, vui lòng nhập tay”).

#### 4.2. Gợi ý cấu trúc bảng AI Draft Order

Tên bảng có thể là `ai_draft_order` hoặc `orders` với `order_type = 'ai_draft'`. Gợi ý các cột:

- `id`
- `business_id`
- `employee_id`
- `customer_id` *(nullable)*
- `items` *(JSON)*  
  - Danh sách items như trong `draft_order.items`.
- `payment_type` (`cash` / `debt` / `unknown`)
- `ai_confidence` *(float)*
- `ai_issues` *(JSON)*
- `status` (`draft` | `needs_review` | `rejected` | `confirmed`)
- `ai_raw_request` *(JSON)*  
  - Lưu toàn bộ payload gửi sang AI (phục vụ debugging & phân tích sau).
- `ai_raw_response` *(JSON)*  
  - Lưu toàn bộ response từ AI.
- `created_at`, `updated_at`

---

### 5. Tích hợp với Frontend (Web & Mobile)

> Lưu ý: Frontend **không gọi trực tiếp AI service**, mà chỉ gọi Backend.

- **Web (Next.js)**:
  - Màn `DraftOrdersPage`:
    - Gọi backend `/api/orders/draft` (hoặc tương tự) để lấy danh sách draft orders.
    - Hiển thị items, khách hàng, payment, `ai_confidence`, `issues` để owner/nhân viên review.
  - Màn `CreateOrderPage`:
    - Có thể bổ sung nút “Nhập câu lệnh AI” (text) để backend gọi AI.
- **Mobile (Flutter)**:
  - Màn “Voice Order”:
    - Ghi âm → upload audio lên backend.
    - Backend gọi AI theo contract trong tài liệu này.
    - Mobile chỉ hiển thị draft trả về từ backend (sau khi backend đã lưu DB hoặc trước khi lưu).

---

### 6. Acceptance Criteria cho TASK-HUY-01

- Tài liệu này được commit trong repo tại `docs/api/ai-draft-order-contract.md`.
- Backend & AI dev đọc và **hiểu rõ**:
  - Endpoint `/ai/v1/draft-orders/parse`.
  - Request/response schema & error code.
  - Cách mapping sang bảng `AI_draft_order` và flow hiển thị trên frontend.
- Mọi thay đổi sau này cho contract phải cập nhật lại tài liệu này và thông báo cho các bên liên quan.

