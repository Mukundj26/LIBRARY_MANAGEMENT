-- Dropping tables in reverse order of dependencies
DROP TABLE IF EXISTS system_logs;
DROP TABLE IF EXISTS fines;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS admins;

CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(512) NOT NULL
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    category_id INTEGER,
    qty INTEGER NOT NULL DEFAULT 1,
    available_qty INTEGER NOT NULL DEFAULT 1,
    created_by VARCHAR(255),
    notes TEXT,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    joined_date DATE NOT NULL,
    password_hash VARCHAR(512),
    created_by VARCHAR(255),
    notes TEXT
);

CREATE TABLE issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'issued',
    processed_by VARCHAR(255),
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(member_id) REFERENCES members(id)
);

CREATE TABLE fines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    paid_status VARCHAR(20) NOT NULL DEFAULT 'unpaid',
    date_assessed DATE NOT NULL,
    FOREIGN KEY(issue_id) REFERENCES issues(id),
    FOREIGN KEY(member_id) REFERENCES members(id)
);

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    reservation_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(member_id) REFERENCES members(id)
);

CREATE TABLE system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    action_type VARCHAR(50),
    target_table VARCHAR(50),
    user_name VARCHAR(255),
    description TEXT
);

-- Seed Data
INSERT INTO admins (username, password_hash)
VALUES ('admin', 'scrypt:32768:8:1$PXbX41uxbqjGDdhL$8f2984e1e63e585240aa983f9dd09a5ede74288d40aadac1428e9778ea05d75d2c225cae649108bcc0e35ed9f11aed0e95221f9ecdd175528cb02546b42c4d68');

INSERT INTO categories (name) VALUES ('Fiction'), ('Science'), ('Technology'), ('History');

INSERT INTO books (title, author, isbn, category_id, qty, available_qty) VALUES 
('1984', 'George Orwell', '978-0451524935', 1, 5, 5),
('A Brief History of Time', 'Stephen Hawking', '978-0553380163', 2, 3, 3),
('Clean Code', 'Robert C. Martin', '978-0132350884', 3, 2, 2);

INSERT INTO members (name, email, phone, joined_date) VALUES 
('John Doe', 'john.doe@example.com', '1234567890', '2023-01-15'),
('Jane Smith', 'jane.smith@example.com', '0987654321', '2023-02-20');
