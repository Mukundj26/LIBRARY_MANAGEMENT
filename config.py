import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-library'
    
    # SQLite Configuration (Pointed to LibraryManagement folder so VS Code sees the same DB)
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'LibraryManagement', 'database', 'library.db')
    
    # Library Rules
    FINE_RATE_PER_DAY = 2.0  # ₹2/day
    LOAN_PERIOD_DAYS = 14
    MAX_BOOKS_PER_MEMBER = 3
