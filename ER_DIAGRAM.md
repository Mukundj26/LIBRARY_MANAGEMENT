# Entity Relationship Diagram (ERD)

This document provides the ER diagram for the Library Management System database.

## Database Schema Diagram

```mermaid
erDiagram
    ADMINS ||--o{ SYSTEM_LOGS : "performed_by"
    CATEGORIES ||--o{ BOOKS : "contains"
    BOOKS ||--o{ ISSUES : "issued"
    BOOKS ||--o{ RESERVATIONS : "reserved"
    MEMBERS ||--o{ ISSUES : "borrows"
    MEMBERS ||--o{ FINES : "owes"
    MEMBERS ||--o{ RESERVATIONS : "requests"
    ISSUES ||--o| FINES : "incurs"

    ADMINS {
        int id PK "Primary Key"
        string username "Unique Username"
        string password_hash "Hashed Password"
    }

    CATEGORIES {
        int id PK "Primary Key"
        string name "Category Name"
    }

    BOOKS {
        int id PK "Primary Key"
        string title "Book Title"
        string author "Author Name"
        string isbn "Unique ISBN"
        int category_id FK "References Categories"
        int qty "Total Quantity"
        int available_qty "Available Quantity"
        string created_by "Admin who added"
        text notes "Optional Notes"
    }

    MEMBERS {
        int id PK "Primary Key"
        string name "Member Name"
        string email "Unique Email"
        string phone "Phone Number"
        date joined_date "Joining Date"
        string password_hash "Hashed Password"
        string created_by "Admin who added"
        text notes "Optional Notes"
    }

    ISSUES {
        int id PK "Primary Key"
        int book_id FK "References Books"
        int member_id FK "References Members"
        date issue_date "Date Issued"
        date due_date "Expected Return"
        date return_date "Actual Return"
        string status "issued/returned/etc"
        string processed_by "Admin Name"
    }

    FINES {
        int id PK "Primary Key"
        int issue_id FK "References Issues"
        int member_id FK "References Members"
        decimal amount "Fine Amount"
        string paid_status "paid/unpaid"
        date date_assessed "Date Assessed"
    }

    RESERVATIONS {
        int id PK "Primary Key"
        int book_id FK "References Books"
        int member_id FK "References Members"
        date reservation_date "Date Requested"
        string status "active/fulfilled/cancelled"
    }

    SYSTEM_LOGS {
        int id PK "Primary Key"
        datetime timestamp "Log Time"
        string action_type "Action Performed"
        string target_table "Affected Table"
        string user_name "User who performed"
        text description "Detailed Info"
    }
```

## Relationships Summary

1.  **Categories to Books**: Each category can contain multiple books.
2.  **Books to Issues**: A book can be issued multiple times over its lifetime.
3.  **Members to Issues**: A member can borrow multiple books.
4.  **Issues to Fines**: An issue may result in at most one fine if returned late.
5.  **Members to Fines**: A member can have multiple fines across different issues.
6.  **Books to Reservations**: Multiple members can reserve the same book if unavailable.
7.  **Members to Reservations**: A member can make multiple reservations.
8.  **System Logs**: Tracks actions performed across various tables, usually associated with an admin's username.
