from flask import Blueprint, render_template, session, redirect, url_for, flash
from db import query_db
from routes.auth import login_required, admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/logs')
@login_required
@admin_required
def logs():
    # Fetch recent system logs
    activity_logs = query_db('SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT 100')
    
    # Fetch raw data for each table
    raw_books = query_db('SELECT * FROM books')
    raw_members = query_db('SELECT * FROM members')
    raw_issues = query_db('SELECT * FROM issues')
    
    return render_template('logs.html', 
                          logs=activity_logs, 
                          books=raw_books, 
                          members=raw_members, 
                          issues=raw_issues)
