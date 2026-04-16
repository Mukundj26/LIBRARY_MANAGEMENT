# 📚 Premium Library Management System

A robust, multi-role library management platform built with **Python/Flask** and **SQLite**. This system is designed for both administrators and library members, featuring automated transaction tracking, fine calculations, and a high-performance database audit tail.

---

## 🚀 Key Features

### 👤 Multi-Role Authentication
- **Library Admins:** Full control over books, members, and system logs.
- **Member Access:** Self-service registration and a personal dashboard to track borrowed books and fines.

### 📖 Advanced Book Management
- **Catalog Tracking:** Detailed storage of titles, authors, categories, and ISBNs.
- **Dynamic Availability:** Real-time quantity updates when books are issued or returned.
- **Metadata Support:** Store internal "Notes / Remarks" for any book.

### 🤝 Member & Transaction Suite
- **Registration:** Instant account creation for new members.
- **Issuance Logic:** Easily "Issue" books to members with automated due-date calculation.
- **Return & Fine System:** Automatic fine generation (₹2/day) for overdue books upon return.

### 🛡️ System Audit & Logging
- **Action Tracking:** Every database change (Add, Edit, Issue) records **who** did it and **when**.
- **System Logs Page:** A dedicated Admin-only interface to view the live activity feed and browse raw table data.

---

## 🏗️ Architecture & Tech Stack

- **Backend:** Flask (Python) with a modular blueprint architecture.
- **Database:** SQLite (`library.db`) for a portable, single-file storage solution.
- **Frontend:** Vanilla CSS (Modern UI) with rich aesthetics, glassmorphism elements, and responsive tables.
- **Security:** Secure password hashing using `werkzeug.security`.

### Database Schema
The system uses 8 primary tables:
1. `admins`: Administrative credentials.
2. `categories`: Book classifications.
3. `books`: Detailed catalog with inventory tracking.
4. `members`: User profiles with login capability.
5. `issues`: The transaction bridge between books and members.
6. `fines`: Financial tracking for overdue returns.
7. `reservations`: Book hold management.
8. `system_logs`: The central audit trail for all system events.

---

## 🔄 Common Workflows

### 1. Adding a New Book
- Log in as **Admin**.
- Navigate to **Books** -> **Add New Book**.
- Fill in details and add any internal "Notes".
- The system automatically logs your username as the creator.

### 2. Registering and Issuing
- A new user uses the **Register** link to create a Member account.
- The Admin navigates to **Issuance** -> **Process New Issue**.
- Select the book and member. The system calculates the due date and records the Admin who processed it.

### 3. Returning & Fines
- Go to **Issuance** -> **Returned**.
- Click the "Return" icon.
- If overdue, the system generates a **Fine** record and displays it in the **Fines** section.

---

## 🛠️ Installation & Setup

1. **Clone the project** to your local machine.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the Database:**
   The `library.db` is included, but to reset it, run:
   ```bash
   python -c "from app import create_app; from db import init_db; init_db(create_app())"
   ```
4. **Run the Application:**
   ```bash
   python app.py
   ```
5. **Access the site:** Open `http://127.0.0.1:5000` in your browser.

---

## 📂 Project Structure
```text
├── app.py              # Entry point & blueprint registration
├── config.py           # System rules & DB paths
├── db.py               # Database utility layer (SQLite)
├── routes/             # Backend logic (Auth, Books, Members, etc.)
├── static/             # CSS styling & Frontend assets
├── templates/          # HTML views
└── database/
    ├── schema.sql      # SQL blueprint
    └── library.db      # The single-file database
```

*Developed as a high-performance solution for modern library management.*
