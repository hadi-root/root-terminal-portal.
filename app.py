import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session
from init_db import init_db

app = Flask(__name__)
app.secret_key = "root_super_secure_vault_key"

DB_FILE = "database.db"

def get_db_connection():
    # Automatically initialize the database if the file is missing
    if not os.path.exists(DB_FILE):
        init_db()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Allows us to access columns by name like dictionary keys
    return conn

def load_site_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM settings')
    rows = cursor.fetchall()
    conn.close()
    
    # Convert SQL rows into a clean Python dictionary for Jinja templates
    data = {}
    for row in rows:
        key = row['key']
        val = row['value']
        
        # Process comma-separated tags or newline-separated milestones into lists
        if key == 'badges':
            data[key] = [b.strip() for b in val.split(',') if b.strip()]
        elif key == 'milestones':
            data[key] = [m.strip() for m in val.split('\n') if m.strip()]
        elif key.startswith('skill_'):
            data[key] = int(val) if val.isdigit() else 0
        else:
            data[key] = val
            
    return data

def update_db_setting(cursor, key, value):
    cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))

@app.route('/')
def index():
    site_data = load_site_data()
    return render_template('index.html', data=site_data)

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    site_data = load_site_data()
    
    ADMIN_USERNAME = "RTH"
    ADMIN_PASSWORD = "@4560082010"

    if request.method == 'POST':
        if 'login_form' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                return "<h1 style='color:#ff3333; font-family:monospace; text-align:center; margin-top:50px;'>Authentication Failure: Invalid Parameters</h1>", 401

        elif 'global_update' in request.form:
            if not session.get('logged_in'):
                return "Unauthorized Action", 403
                
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Update each setting line-by-line inside the SQL table
            update_db_setting(cursor, "name", request.form.get('name'))
            update_db_setting(cursor, "title", request.form.get('title'))
            update_db_setting(cursor, "bio", request.form.get('bio'))
            update_db_setting(cursor, "badges", request.form.get('badges'))
            update_db_setting(cursor, "milestones", request.form.get('milestones'))
            
            update_db_setting(cursor, "repo_title_1", request.form.get('repo_title_1'))
            update_db_setting(cursor, "repo_desc_1", request.form.get('repo_desc_1'))
            update_db_setting(cursor, "repo_title_2", request.form.get('repo_title_2'))
            update_db_setting(cursor, "repo_desc_2", request.form.get('repo_desc_2'))
            
            update_db_setting(cursor, "metric_1", request.form.get('metric_1'))
            update_db_setting(cursor, "metric_2", request.form.get('metric_2'))
            update_db_setting(cursor, "metric_3", request.form.get('metric_3'))
            update_db_setting(cursor, "metric_4", request.form.get('metric_4'))
            
            update_db_setting(cursor, "skill_py", request.form.get('skill_py', 0))
            update_db_setting(cursor, "skill_flask", request.form.get('skill_flask', 0))
            update_db_setting(cursor, "skill_html", request.form.get('skill_html', 0))
            update_db_setting(cursor, "skill_css", request.form.get('skill_css', 0))
            update_db_setting(cursor, "skill_git", request.form.get('skill_git', 0))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    if not session.get('logged_in'):
        return render_template('admin_login.html')
        
    # Before displaying to the admin panel inputs, convert back to editable raw text configurations
    raw_data = dict(site_data)
    # Reload original text block structures for editing textareas cleanly
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key='badges'")
    row = c.fetchone()
    if row: raw_data['badges'] = row['value']
    c.execute("SELECT value FROM settings WHERE key='milestones'")
    row = c.fetchone()
    if row: raw_data['milestones'] = row['value']
    conn.close()

    return render_template('admin.html', data=raw_data)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)