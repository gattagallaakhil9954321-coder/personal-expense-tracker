import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response
import sqlite3, csv, io
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'expenses.db'
app = Flask(__name__)
app.secret_key = 'change-this-secret-key-before-deployment'

CATEGORIES = ['Food', 'Transport', 'Shopping', 'Bills', 'Education', 'Health', 'Entertainment', 'Other']

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            note TEXT DEFAULT ''
        )''')

@app.route('/')
def index():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    sql = 'SELECT * FROM expenses WHERE 1=1'
    params = []
    if search:
        sql += ' AND (title LIKE ? OR note LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    if category in CATEGORIES:
        sql += ' AND category = ?'
        params.append(category)
    if start_date:
        sql += ' AND expense_date >= ?'
        params.append(start_date)
    if end_date:
        sql += ' AND expense_date <= ?'
        params.append(end_date)
    sql += ' ORDER BY expense_date DESC, id DESC'
    with get_db() as conn:
        expenses = conn.execute(sql, params).fetchall()
        total = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0]
        today_total = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE expense_date = ?', (date.today().isoformat(),)).fetchone()[0]
        count = conn.execute('SELECT COUNT(*) FROM expenses').fetchone()[0]
        category_rows = conn.execute('SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC').fetchall()
    return render_template('index.html', expenses=expenses, categories=CATEGORIES,
        total=total, today_total=today_total, count=count, category_rows=category_rows,
        filters={'search': search, 'category': category, 'start_date': start_date, 'end_date': end_date})

@app.route('/add', methods=['POST'])
def add_expense():
    title = request.form.get('title', '').strip()
    amount_text = request.form.get('amount', '').strip()
    category = request.form.get('category', '')
    expense_date = request.form.get('expense_date', '')
    note = request.form.get('note', '').strip()
    try:
        amount = float(amount_text)
    except ValueError:
        amount = 0
    if not title or amount <= 0 or category not in CATEGORIES or not expense_date:
        flash('Enter a title, a positive amount, a valid category and a date.', 'error')
        return redirect(url_for('index'))
    with get_db() as conn:
        conn.execute('INSERT INTO expenses (title, amount, category, expense_date, note) VALUES (?, ?, ?, ?, ?)',
                     (title, amount, category, expense_date, note))
    flash('Expense added successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    with get_db() as conn:
        conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    flash('Expense deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/export')
def export_csv():
    with get_db() as conn:
        rows = conn.execute('SELECT title, amount, category, expense_date, note FROM expenses ORDER BY expense_date DESC').fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Amount', 'Category', 'Date', 'Note'])
    for row in rows:
        writer.writerow([row['title'], f"{row['amount']:.2f}", row['category'], row['expense_date'], row['note']])
    return Response('\ufeff' + output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=expenses.csv'})

init_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
