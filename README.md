# BizFlow - Digital Transformation Platform for Household Businesses

![Project Status](https://img.shields.io/badge/Status-Development-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)
![Team](https://img.shields.io/badge/Team-7Members-orange)

**BizFlow** is a comprehensive solution designed to modernize traditional household businesses in Vietnam. It combines a Point-of-Sale (POS) system with an AI-powered assistant to automate ordering via voice/text and streamline bookkeeping in compliance with **Circular 88/2021/TT-BTC**.

---

## 📑 Table of Contents
- [Context & Problem](#-context--problem)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Development Process](#-development-process)
- [Team Members](#-team-members)

---

## 📖 Context & Problem
Household businesses in Vietnam often operate manually, leading to calculation errors, inventory losses, and difficulty in tracking customer debts. Existing POS solutions are often too complex, expensive, or not tailored to the specific needs of hardware/construction material stores (Group 1 & 2 under Ministry of Finance).

**BizFlow Solution:**
- **Voice-to-Order:** AI assistant listens to natural language and creates draft orders.
- **Auto-Bookkeeping:** Automatically generates financial reports required by Vietnamese law (Circular 88).
- **Hybrid Platform:** Works on Mobile (for employees on the move) and Web (for owners managing back-office).

---

## 🚀 Key Features

### 🛒 For Employee (Mobile App)
- **Quick POS:** Search products, add to cart, and print receipts.
- **Voice Order (AI):** Record voice commands to generate draft orders automatically.
- **Debt Recording:** Record credit sales for registered customers.
- **Real-time Notifications:** Receive alerts when AI finishes processing an order.

### 🏢 For Owner (Web Dashboard)
- **Inventory Management:** Track stock levels, import goods.
- **Financial Reporting:** Auto-generated Revenue & Debt reports (Circular 88/2021/TT-BTC).
- **Customer Management:** View purchase history and outstanding debts.
- **Employee Management:** Create accounts and assign roles.

### 🤖 System & AI
- **Speech-to-Text:** Converts Vietnamese voice to text (Whisper).
- **RAG (Retrieval-Augmented Generation):** Maps natural language to exact product SKUs in the database.
- **Auto-Bookkeeping:** Automated ledger entry for every transaction.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Mobile App** | Flutter (Dart), Bloc/Provider |
| **Web Frontend** | Next.js 14, TailwindCSS, Shadcn UI |
| **Backend API** | Python (FastAPI/Django), Clean Architecture |
| **AI Service** | Python, LangChain, ChromaDB, OpenAI/Gemini, Whisper |
| **Database** | PostgreSQL (Primary), Redis (Caching) |
| **DevOps** | Docker, Docker Compose, GitHub Actions |

---

## 📂 Project Structure

This project follows a **Monorepo** structure:

```
software-engineering-project/
├── backend/          # Python Backend Source Code (API, Auth, Logic)
├── frontend-web/     # Next.js Web Application (Admin/Owner Dashboard)
├── mobile-app/       # Flutter Mobile Application (POS for Employee)
├── ai-service/       # AI Logic (RAG, Speech-to-Text processing)
├── docs/             # Documentation (SRS, SDD, Test Plans, Slide)
├── docker-compose.yml # Container orchestration
└── README.md         # General documentation
```

---

## ⚡ Getting Started

### Prerequisites
Ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Docker & Docker Compose](https://www.docker.com/)
- [Python 3.10+](https://www.python.org/)
- [Node.js 20+](https://nodejs.org/)
- [Flutter SDK](https://flutter.dev/)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/software-engineering-project.git
cd software-engineering-project
```

### 2. Setup Backend & Database
```bash
cd backend
# Create virtual environment
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
# Run Docker for DB
docker-compose up -d
# Run Server
python main.py
```

### 3. Setup Frontend (Web)
```bash
cd frontend-web
npm install
npm run dev
```

### 4. Setup Mobile App
```bash
cd mobile-app
flutter pub get
flutter run
```

---

## 🔄 Development Process (Git Flow)

We strictly follow **Git Flow** for collaboration.

1.  **`main`**: Production-ready code. **DO NOT PUSH DIRECTLY.**
2.  **`develop`**: Integration branch. All features merge here first.
3.  **`feature/feature-name`**: Working branch for each member.

**Workflow:**
1.  Checkout `develop` and pull latest: `git checkout develop && git pull`.
2.  Create feature branch: `git checkout -b feature/login-screen`.
3.  Commit changes: `git commit -m "feat: add login UI"`.
4.  Push to origin: `git push origin feature/login-screen`.
5.  **Create a Pull Request (PR)** on GitHub to merge into `develop`.

---

## 👥 Team Members (Group 4Bees)

| Student ID | Name | Role |
| :--- | :--- | :--- |
| **087205004266** | **Huỳnh Xuân Huy** | Leader / Project Manager / AI Engineer |
| **0582066001036** | **Lê Ngọc Châu** | Business Analyst / Tester / Web Developer
| **068206002643** | **Njan Bruy** | Backend Developer |
| **086206000986** | **Lê Hà Quốc Huy** | Backend Developer |
| **0862001763** | **Lưu Võ Thiên Phúc** | Backend Developer / Mobile Developer |
| **079206042023** | **Nguyễn Phúc Cảnh** | Backend Developer / Mobile Developer |