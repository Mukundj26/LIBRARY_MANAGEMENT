from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from db import query_db, execute_db, log_activity
from datetime import date
from routes.auth import login_required

members_bp = Blueprint('members', __name__)

@members_bp.route('/members')
@login_required
def index():
    return render_template('members.html')

@members_bp.route('/api/members/search')
@login_required
def search():
    query = request.args.get('q', '')
    members = query_db('SELECT * FROM members WHERE name LIKE ? OR email LIKE ?', [f'%{query}%', f'%{query}%'])
    return jsonify([dict(m) for m in members])

@members_bp.route('/members/add', methods=['POST'])
@login_required
def add():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    notes = request.form.get('notes', '')
    joined_date = date.today().isoformat()
    created_by = session.get('username', 'System')
    
    try:
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
            
        execute_db('INSERT INTO members (name, email, phone, joined_date, created_by, notes) VALUES (?, ?, ?, ?, ?, ?)',
                   [name, email, phone, joined_date, created_by, notes])
        log_activity('REGISTER', 'members', created_by, f"Registered new member: {name} ({email})")
        flash('Member registered successfully!')
    except ValueError as ve:
        flash(str(ve))
    except Exception as e:
        flash(f'Error registering member: {str(e)}')
        
    return redirect(url_for('members.index'))

@members_bp.route('/members/history/<int:id>')
@login_required
def history(id):
    member = query_db('SELECT * FROM members WHERE id = ?', [id], one=True)
    history = query_db('''
        SELECT i.*, b.title 
        FROM issues i 
        JOIN books b ON i.book_id = b.id 
        WHERE i.member_id = ? 
        ORDER BY i.issue_date DESC
    ''', [id])
    return jsonify({
        'member': dict(member),
        'history': [dict(h) for h in history]
    })
@members_bp.route('/members/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    notes = request.form.get('notes', '')
    
    try:
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
            
        execute_db('UPDATE members SET name = ?, email = ?, phone = ?, notes = ? WHERE id = ?',
                   [name, email, phone, notes, id])
        log_activity('EDIT', 'members', session.get('username', 'System'), f"Updated member ID {id}: {name}")
        flash('Member updated successfully!')
    except ValueError as ve:
        flash(str(ve))
    except Exception as e:
        flash(f'Error updating member: {str(e)}')
    return redirect(url_for('members.index'))
