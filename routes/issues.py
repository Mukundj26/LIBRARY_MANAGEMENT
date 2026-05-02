from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from db import query_db, execute_db, log_activity
from datetime import date, datetime, timedelta
from config import Config
from routes.auth import login_required

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/issues')
@login_required
def index():
    issues = query_db('''
        SELECT i.*, b.title, m.name as member_name 
        FROM issues i 
        JOIN books b ON i.book_id = b.id 
        JOIN members m ON i.member_id = m.id 
        WHERE i.status = 'issued'
    ''')
    return render_template('issues.html', issues=issues)

@issues_bp.route('/issues/add', methods=['POST'])
@login_required
def add():
    book_id = request.form['book_id']
    member_id = request.form['member_id']
    
    # Check if book is available
    book = query_db('SELECT available_qty FROM books WHERE id = ?', [book_id], one=True)
    if not book or book['available_qty'] <= 0:
        flash('Book not available for issue!')
        return redirect(url_for('issues.index'))
    
    # Check member limit
    current_issues = query_db("SELECT COUNT(*) as count FROM issues WHERE member_id = ? AND status = 'issued'", [member_id], one=True)
    if current_issues['count'] >= Config.MAX_BOOKS_PER_MEMBER:
        flash(f'Member has already reached max limit of {Config.MAX_BOOKS_PER_MEMBER} books!')
        return redirect(url_for('issues.index'))

    issue_date = date.today()
    due_date = issue_date + timedelta(days=Config.LOAN_PERIOD_DAYS)
    processed_by = session.get('username', 'System')
    
    execute_db('INSERT INTO issues (book_id, member_id, issue_date, due_date, status, processed_by) VALUES (?, ?, ?, ?, ?, ?)',
               [book_id, member_id, issue_date.isoformat(), due_date.isoformat(), 'issued', processed_by])
    
    log_activity('ISSUE', 'issues', processed_by, f"Issued book ID {book_id} to member ID {member_id}")
    
    execute_db('UPDATE books SET available_qty = available_qty - 1 WHERE id = ?', [book_id])
    
    flash('Book issued successfully!')
    return redirect(url_for('issues.index'))

@issues_bp.route('/issues/return/<int:id>', methods=['POST'])
@login_required
def return_book(id):
    issue = query_db('SELECT * FROM issues WHERE id = ?', [id], one=True)
    if not issue or issue['status'] == 'returned':
        return redirect(url_for('issues.index'))
    
    return_date = date.today()
    due_date = issue['due_date']
    if isinstance(due_date, str):
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    
    execute_db("UPDATE issues SET return_date = ?, status = 'returned' WHERE id = ?", [return_date.isoformat(), id])
    execute_db('UPDATE books SET available_qty = available_qty + 1 WHERE id = ?', [issue['book_id']])
    
    log_activity('RETURN', 'issues', session.get('username', 'System'), f"Returned book ID {issue['book_id']} for issue ID {id}")
    
    # Calculate Fine
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        fine_amount = overdue_days * Config.FINE_RATE_PER_DAY
        execute_db('INSERT INTO fines (issue_id, member_id, amount, paid_status, date_assessed) VALUES (?, ?, ?, ?, ?)',
                   [id, issue['member_id'], fine_amount, 'unpaid', return_date.isoformat()])
        flash(f'Book returned. A fine of ₹{fine_amount} has been generated.')
    else:
        flash('Book returned successfully!')
        
    return redirect(url_for('issues.index'))
