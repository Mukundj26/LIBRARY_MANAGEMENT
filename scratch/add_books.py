import sqlite3

def add_data():
    conn = sqlite3.connect('d:/lib/database/library.db')
    cursor = conn.cursor()
    
    # Add Categories
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Motivation')")
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Engineering')")
    
    cursor.execute("SELECT id FROM categories WHERE name='Motivation'")
    mot_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM categories WHERE name='Engineering'")
    eng_id = cursor.fetchone()[0]
    
    books = [
        # Motivation
        ('The 7 Habits of Highly Effective People', 'Stephen R. Covey', '978-0743269513', mot_id, 3, 3),
        ('Atomic Habits', 'James Clear', '978-0735211292', mot_id, 5, 5),
        ('Mindset: The New Psychology of Success', 'Carol S. Dweck', '978-0345472328', mot_id, 4, 4),
        ('Think and Grow Rich', 'Napoleon Hill', '978-1585424337', mot_id, 2, 2),
        ('Drive: The Surprising Truth About What Motivates Us', 'Daniel H. Pink', '978-1594484803', mot_id, 3, 3),
        ('Awaken the Giant Within', 'Tony Robbins', '978-0671791544', mot_id, 3, 3),
        ('The Power of Habit', 'Charles Duhigg', '978-0812981605', mot_id, 2, 2),
        ('Grit: The Power of Passion and Perseverance', 'Angela Duckworth', '978-1501111105', mot_id, 4, 4),
        ('Man''s Search for Meaning', 'Viktor E. Frankl', '978-0807014271', mot_id, 5, 5),
        ('Can''t Hurt Me', 'David Goggins', '978-1544512280', mot_id, 3, 3),
        ('Outliers: The Story of Success', 'Malcolm Gladwell', '978-0316017930', mot_id, 2, 2),
        
        # Engineering
        ('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033848', eng_id, 2, 2),
        ('The Pragmatic Programmer', 'Andrew Hunt', '978-0201616224', eng_id, 4, 4),
        ('Design Patterns: Elements of Reusable Object-Oriented Software', 'Erich Gamma', '978-0201633610', eng_id, 3, 3),
        ('Code Complete: A Practical Handbook of Software Construction', 'Steve McConnell', '978-0735619678', eng_id, 2, 2),
        ('Structure and Interpretation of Computer Programs', 'Harold Abelson', '978-0262510875', eng_id, 1, 1),
        ('Engineering Mechanics: Dynamics', 'J.L. Meriam', '978-1118885840', eng_id, 2, 2),
        ('Fundamentals of Thermodynamics', 'Claus Borgnakke', '978-1118131992', eng_id, 3, 3),
        ('Shigley''s Mechanical Engineering Design', 'Richard G Budynas', '978-0073398204', eng_id, 4, 4),
        ('Control Systems Engineering', 'Norman S. Nise', '978-1118170519', eng_id, 2, 2),
        ('Materials Science and Engineering: An Introduction', 'William D. Callister Jr.', '978-1118319222', eng_id, 5, 5),
        ('Clean Architecture', 'Robert C. Martin', '978-0134494166', eng_id, 3, 3),
    ]
    
    for b in books:
        try:
            cursor.execute("INSERT INTO books (title, author, isbn, category_id, qty, available_qty) VALUES (?, ?, ?, ?, ?, ?)", b)
        except sqlite3.IntegrityError:
            pass # Book might already exist
            
    conn.commit()
    conn.close()
    print("Done adding books.")

if __name__ == '__main__':
    add_data()
