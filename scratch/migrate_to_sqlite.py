import pymysql
import sqlite3
import os

# MySQL Credentials (Hardcoded for migration only)
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Mukund@2006',
    'database': 'library_db'
}

SQLITE_PATH = 'database/library.db'
SCHEMA_PATH = 'database/schema.sql'

def migrate():
    print("Starting migration from MySQL to SQLite...")
    
    # 1. Initialize SQLite Database
    if not os.path.exists('database'):
        os.makedirs('database')
    
    if os.path.exists(SQLITE_PATH):
        os.remove(SQLITE_PATH)
        print("Removed existing library.db")

    lite_conn = sqlite3.connect(SQLITE_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        lite_conn.executescript(f.read())
    print("Initialized SQLite schema.")

    # 2. Connect to MySQL
    mysql_conn = pymysql.connect(**MYSQL_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    
    tables = ['admins', 'categories', 'books', 'members', 'issues', 'fines', 'reservations', 'system_logs']
    
    try:
        for table in tables:
            print(f"Migrating table: {table}")
            with mysql_conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
            
            if not rows:
                print(f"No data in {table}")
                continue
            
            # Get columns
            cols = rows[0].keys()
            placeholders = ', '.join(['?'] * len(cols))
            col_names = ', '.join(cols)
            
            # Clear default seed data from SQLite before importing MySQL data
            lite_conn.execute(f"DELETE FROM {table}")
            
            # Insert into SQLite
            insert_sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
            for row in rows:
                values = [row[col] for col in cols]
                lite_conn.execute(insert_sql, values)
            
        lite_conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        mysql_conn.close()
        lite_conn.close()

if __name__ == "__main__":
    migrate()
