# PROJECT PROPOSAL: BizFlow

## 1. Project Information
*   **English Name:** Platform to support digital transformation for household businesses.
*   **Vietnamese Name:** Nền tảng hỗ trợ chuyển đổi số cho hộ kinh doanh.
*   **Abbreviation:** BizFlow
*   **Team:** 7Members

---

## 2. Context & Problem Statement

### a. Context
In Vietnam, household businesses play a critical role in the local economy, especially in traditional sectors such as building materials, construction supplies, and hardware retail. The majority of these fall under Group 1 or Group 2 classifications as defined by the Ministry of Finance's Decision 3389/QĐ-BTC (2025).

### b. Current Problems
*   **Manual Workflows:** Daily tasks (sales recording, inventory, debt tracking) are performed with handwritten notebooks or simple Excel files.
*   **Lack of Resources:** Most businesses lack the budget to hire professional accountants.
*   **Incompatible Solutions:** Existing POS systems are designed for restaurants/fashion or large enterprises. They fail to address specific needs like:
    *   Multi-channel orders (counter, phone, Zalo).
    *   Long-term customer debt management.
    *   Low digital literacy of owners.
*   **Hardware Limitations:** Many operate with only a single smartphone, lacking computers, scanners, or printers required by complex POS systems.
*   **Consequences:** Errors in calculation, difficulty tracking inventory/debt, and lack of business insights.

### c. Solution Vision
We propose **BizFlow**, a comprehensive system designed specifically for traditional stores.
*   **Core Innovation:** Integrates an AI-powered assistant capable of understanding natural language requests (Voice/Text) to automatically create draft orders.
*   **Automation:** Auto-fills data into templates and performs bookkeeping automatically.
*   **Goal:** Reduce human errors, support automation, and provide real-time visibility into operations.

---

## 3. Proposed Solution

Build an application (Mobile & Web) supporting the following core functionalities:

### 3.1. Actors
1.  **Employee:** Sales staff creating orders at the counter.
2.  **Owner:** Business owner managing the entire operation.
3.  **Administrator:** System admin managing the platform.
4.  **System:** The automated logic (AI & Bookkeeping).

### 3.2. Functional Requirements

#### 🛒 Employee
*   **Login:** Access system via account.
*   **Create At-Counter Orders:** Quick search, select quantity, assign customers, add to cart (supports shortcuts/filtering).
*   **Record Debt:** Record debt directly during order creation for registered customers.
*   **Print Sales Orders:** Generate and print bills via connected printers.
*   **Real-Time Notifications:** Receive immediate alerts when AI/Chatbot generates a draft order.
*   **Confirm AI Orders:** Review and confirm "Draft Orders" created by the AI assistant.

#### 🏢 Owner
*(Includes all Employee permissions)*
*   **Product Catalog:** Create/Update/Disable products (name, image, price, multi-units).
*   **Inventory Management:** Record imports, track real-time stock, view history.
*   **Customer Management:** Manage info, purchase history, outstanding debts, payment logs.
*   **Reports & Analytics:** Dashboard for daily/monthly revenue, best-sellers, low-stock alerts.
*   **Employee Management:** Create accounts, reset passwords, audit logs.

#### 🤖 System & AI
*   **Natural Language Processing (NLP):** Convert voice/text (e.g., *"get 5 cement bags for Mr. Ba, put it on his tab"*) into a structured Draft Order.
*   **Auto-Bookkeeping:** Automatically perform bookkeeping for every transaction.
*   **Compliance:** Generate reports required by **Circular 88/2021/TT-BTC** (Detailed Revenue Ledger, Business Operations Report). Templates are continuously updated to match regulations.

#### 🛠 Administrator
*   **Owner Account Management:** Activate/Deactivate household business accounts.
*   **Subscription Pricing:** Manage pricing plans (Basic, Pro).
*   **Platform Analytics:** Monitor global system health and revenue.
*   **Configuration:** Update master templates for financial reports and global AI settings.

---

## 4. Non-Functional Requirements

1.  **Security & Privacy:**
    *   Protect sensitive sales data.
    *   Strict Role-Based Access Control (RBAC).
2.  **Performance & Scalability:**
    *   Response time < 2000 ms for core actions.
    *   Support large product catalogs and concurrent users.
3.  **Reliability & AI Accuracy:**
    *   Human-in-the-loop: Users must review/confirm AI orders.
    *   Manual fallback available if AI is offline.
4.  **Usability & Accessibility:**
    *   Simple UI suitable for low digital literacy.
    *   Vietnamese interface with Unicode support.
5.  **Compliance:**
    *   Strict adherence to Circular 88/2021/TT-BTC for report generation.

---

## 5. Main Proposal Content

### a. Theory and Practice (Documentation)
Students will apply the software development process and UML 2.0. Deliverables include:
*   User Requirement (UR)
*   Software Requirement Specification (SRS)
*   Architecture & Detailed Design (SDD)
*   System Implementation & Source Code
*   Testing Document (Test Plan/Report)
*   Installation & User Guides

### b. Technology Stack

**Server-side:**
*   **Language:** Python (Clean Architecture).
*   **Database:** MySQL and PostgreSQL.
*   **Caching:** Redis.

**Artificial Intelligence (AI):**
*   **RAG:** ChromaDB, `text-embedding-3-small`.
*   **LLM:** OpenAI / Gemini.
*   **Speech-to-Text:** Google Speech-to-Text / Whisper.

**Client-side:**
*   **Mobile App:** Flutter (with Notification support).
*   **Web Client:** NextJS, Tanstack Query, Shadcn UI, TailwindCSS.

### c. Proposed Tasks (Work Packages)
1.  **Task Package 1:** Deploy databases (MySQL / PostgreSQL).
2.  **Task Package 2:** Set up Clean Architecture with Python.
3.  **Task Package 3:** Develop and deploy the Mobile Application (Flutter).
4.  **Task Package 4:** Develop and deploy the Web Application (NextJS).
