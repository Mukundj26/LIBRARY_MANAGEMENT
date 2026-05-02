from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from db import query_db, execute_db, log_activity
from routes.auth import login_required

books_bp = Blueprint('books', __name__)

@books_bp.route('/books')
@login_required
def index():
    categories = query_db('SELECT * FROM categories')
    return render_template('books.html', categories=categories)

@books_bp.route('/api/books/search')
@login_required
def search():
    query = request.args.get('q', '')
    books = query_db('''
        SELECT b.*, c.name as category_name 
        FROM books b 
        LEFT JOIN categories c ON b.category_id = c.id 
        WHERE b.title LIKE ? OR b.author LIKE ? OR b.isbn LIKE ?
    ''', [f'%{query}%', f'%{query}%', f'%{query}%'])
    return jsonify([dict(b) for b in books])

@books_bp.route('/books/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    category_id = request.form['category_id']
    qty = int(request.form['qty'])
    notes = request.form.get('notes', '')
    created_by = session.get('username', 'System')
    
    try:
        execute_db('INSERT INTO books (title, author, isbn, category_id, qty, available_qty, created_by, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   [title, author, isbn, category_id, qty, qty, created_by, notes])
        log_activity('ADD', 'books', created_by, f"Added new book: {title} (ISBN: {isbn})")
        flash('Book added successfully!')
    except Exception as e:
        flash(f'Error adding book: {str(e)}')
        
    return redirect(url_for('books.index'))

@books_bp.route('/books/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    title = request.form['title']
    author = request.form['author']
    category_id = request.form['category_id']
    qty = int(request.form['qty'])
    notes = request.form.get('notes', '')
    
    # Simple logic: update available_qty based on change in total qty
    book = query_db('SELECT qty, available_qty FROM books WHERE id = ?', [id], one=True)
    diff = qty - book['qty']
    new_available = book['available_qty'] + diff
    
    execute_db('UPDATE books SET title = ?, author = ?, category_id = ?, qty = ?, available_qty = ?, notes = ? WHERE id = ?',
               [title, author, category_id, qty, new_available, notes, id])
    log_activity('EDIT', 'books', session.get('username', 'System'), f"Updated book ID {id}: {title}")
    flash('Book updated successfully!')
    return redirect(url_for('books.index'))
