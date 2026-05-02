# 📚 Premium Library Management System

A robust, multi-role library management platform built with **Python/Flask** and **SQLite**. This system is designed for both administrators and library members, featuring automated transaction tracking, fine calculations, and a high-performance database audit trail.

---

## 🚀 Key Features

### 👤 Multi-Role Authentication & Access Control
- **Administrative Control:** Full CRUD operations for books, member management, and oversight of system-wide audit logs.
- **Member Portals:** Self-service registration allowing users to track their own borrowed history and pending fines.
- **Secure Persistence:** Powered by SQLite with secure password hashing via `werkzeug.security`.

### 📖 Advanced Book & Inventory Management
- **Smart Cataloging:** Store extensive metadata including Titles, Authors, ISBNs, and internal "Notes/Remarks".
- **Dynamic Inventory Tracking:** Automated "Available Quantity" management that shifts in real-time as books are issued and returned.
- **Diverse Categorization:** Pre-configured with categories such as **Fiction**, **Science**, **Technology**, **History**, **Motivation**, and **Engineering**.
- **Real-time Search:** AJAX-powered search bar for instant title/author/ISBN lookups without page reloads.

### 🤝 Transaction Logic & Due Date Management
- **Issuance Guardrails:** Enforces a maximum limit of **3 books** per member and checks for stock availability before processing.
- **Automated Due Dates:** Configured for a standard **14-day loan period** with automatic calculation upon issuance.
- **Return Processing:** Simple one-click return workflow that restores stock levels instantly.

### 💸 Automated Fine System
- **Overdue Detection:** The system automatically identifies overdue returns.
- **Fine Generation:** Calculates fines at a rate of **₹2 per day** for overdue items.
- **Financial Tracking:** Dedicated fines management section to track payment status for all member accounts.

### 🛡️ Comprehensive Audit Trail
- **System Activity Logging:** Every database mutation (Add, Edit, Issue, Return) is recorded with a timestamp and the initiating user's ID.
- **Admin Audit Interface:** A specialized view for administrators to monitor the live feed of system activities and browse raw data tables for troubleshooting.

---

## 🏗️ Architecture & Tech Stack

- **Backend:** Flask (Python 3) using a clean, Blueprint-based modular architecture.
- **Database:** SQLite (`library.db`) — a lightweight yet powerful single-file database solution.
- **Frontend:** Premium UI design utilizing **Vanilla CSS** for maximum speed and flexibility. Features include:
    - Glassmorphism UI elements
    - Responsive tables and forms
    - Animated transitions and interactive hovers
    - Google Fonts (Inter/Roboto) for modern typography
- **Dependencies:** Managed via `pip` (see `requirements.txt`).

---

## 🔄 Core Workflows

### 1. Catalog Management
Admins can navigate to the **Books** section to add new titles. The system supports bulk entry and allows for detailed notes. The new categories like **Motivation** and **Engineering** are fully integrated.

### 2. The Issue-Return Lifecycle
Registration creates a member profile. Admins then "Issue" books, which automatically reduces the "Available Quantity". Upon "Return", the system calculates if the difference between the return date and due date is positive, triggering a Fine record if necessary.

### 3. Monitoring System Health
Admins use the **Dashboard** for a bird's-eye view of library health (total books vs. available, total members, active issues, and total unpaid fines) and the **Logs** section for deeper security oversight.

---

## 🛠️ Installation & Setup

1. **Clone the project** to your local machine.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the Database:**
   The `library.db` is included, but to reset it to a clean state, run:
   ```bash
   python -c "from app import create_app; from db import init_db; init_db(create_app())"
   ```
4. **Run the Application:**
   ```bash
   python app.py
   ```
5. **Access the platform:** Open `http://127.0.0.1:5000` in your browser.

---

## 📂 Project Structure
```text
├── app.py              # Application factory and blueprint registration
├── config.py           # System settings, limits, and database paths
├── db.py               # Database engine, query utilities, and loggers
├── routes/             # Feature-specific logic (Auth, Books, Fines, etc.)
├── static/             # CSS styling, Modern UI assets, and JavaScript
├── templates/          # Jinja2 HTML templates
└── database/
    ├── schema.sql      # Database blueprint for fresh initialization
    └── library.db      # The production-ready SQLite database
```

*Developed with focus on performance, security, and a premium user experience.*
