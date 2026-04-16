from flask import Blueprint, render_template
from db import query_db
from routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    stats = {
        'total_books': query_db('SELECT SUM(qty) as count FROM books', one=True)['count'] or 0,
        'available_books': query_db('SELECT SUM(available_qty) as count FROM books', one=True)['count'] or 0,
        'total_members': query_db('SELECT COUNT(*) as count FROM members', one=True)['count'] or 0,
        'issued_books': query_db("SELECT COUNT(*) as count FROM issues WHERE status = 'issued'", one=True)['count'] or 0,
        'total_fines': query_db("SELECT SUM(amount) as total FROM fines WHERE paid_status = 'unpaid'", one=True)['total'] or 0
    }
    
    recent_issues = query_db('''
        SELECT i.*, b.title, m.name 
        FROM issues i 
        JOIN books b ON i.book_id = b.id 
        JOIN members m ON i.member_id = m.id 
        ORDER BY i.issue_date DESC LIMIT 5
    ''')
    
    return render_template('dashboard.html', stats=stats, recent_issues=recent_issues)
