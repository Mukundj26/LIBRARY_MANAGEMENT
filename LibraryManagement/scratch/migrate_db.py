import pymysql
from config import Config

def migrate():
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    try:
        with conn.cursor() as cur:
            # Check for columns and add if missing
            tables = {
                'members': [
                    ('password_hash', 'VARCHAR(512) NULL'),
                    ('created_by', 'VARCHAR(255) NULL'),
                    ('notes', 'TEXT NULL')
                ],
                'books': [
                    ('created_by', 'VARCHAR(255) NULL'),
                    ('notes', 'TEXT NULL')
                ],
                'issues': [
                    ('processed_by', 'VARCHAR(255) NULL')
                ]
            }
            
            for table, cols in tables.items():
                cur.execute(f"DESCRIBE {table}")
                existing_cols = [row[0] for row in cur.fetchall()]
                for col_name, col_type in cols:
                    if col_name not in existing_cols:
                        print(f"Adding {col_name} to {table}...")
                        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}")
                    else:
                        print(f"Column {col_name} already exists in {table}")
            
        conn.commit()
        print("Migration successful!")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
