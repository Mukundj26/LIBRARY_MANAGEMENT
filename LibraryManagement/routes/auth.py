from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from db import query_db, execute_db
from datetime import date

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']
        
        # Try Admin first (by username)
        user = query_db('SELECT * FROM admins WHERE username = ?', [username_or_email], one=True)
        role = 'admin'
        
        # If not admin, try Member (by email)
        if not user:
            user = query_db('SELECT * FROM members WHERE email = ?', [username_or_email], one=True)
            role = 'member'
            
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username'] if role == 'admin' else user['name']
            session['role'] = role
            return redirect(url_for('dashboard.index'))
            
        flash('Invalid username/email or password')
        
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        if len(password) < 6:
            flash('Password must be at least 6 characters')
            return render_template('register.html')
            
        existing = query_db('SELECT id FROM members WHERE email = ?', [email], one=True)
        if existing:
            flash('Email already registered')
            return render_template('register.html')
            
        pw_hash = generate_password_hash(password)
        try:
            if len(phone) != 10 or not phone.isdigit():
                raise ValueError("Phone number must be exactly 10 digits.")
                
            execute_db('INSERT INTO members (name, email, phone, joined_date, password_hash, created_by) VALUES (?, ?, ?, ?, ?, ?)',
                      [name, email, phone, date.today().isoformat(), pw_hash, 'Self-Registered'])
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as ve:
            flash(str(ve))
        except Exception as e:
            flash(f'Error during registration: {str(e)}')
            
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required for this action')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function
