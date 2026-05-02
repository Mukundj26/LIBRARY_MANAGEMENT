from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import query_db, execute_db
from routes.auth import login_required

fines_bp = Blueprint('fines', __name__)

@fines_bp.route('/fines')
@login_required
def index():
    fines = query_db('''
        SELECT f.*, m.name as member_name, b.title as book_title
        FROM fines f
        JOIN members m ON f.member_id = m.id
        JOIN issues i ON f.issue_id = i.id
        JOIN books b ON i.book_id = b.id
        ORDER BY f.date_assessed DESC
    ''')
    return render_template('fines.html', fines=fines)

@fines_bp.route('/fines/pay/<int:id>', methods=['POST'])
@login_required
def pay(id):
    execute_db("UPDATE fines SET paid_status = 'paid' WHERE id = ?", [id])
    flash('Fine marked as paid!')
    return redirect(url_for('fines.index'))
