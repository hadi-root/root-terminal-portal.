import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "root_super_secure_vault_key"

DATA_FILE = "site_data.json"

def load_site_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_site_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    site_data = load_site_data()
    return render_template('index.html', data=site_data)

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    site_data = load_site_data()
    
    # Configuration Rules
    ADMIN_USERNAME = "hadi"
    ADMIN_PASSWORD = "hadi_secure_pass"

    if request.method == 'POST':
        # Authentication Gate Form
        if 'login_form' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                return "<h1 style='color:#ff3333; font-family:monospace; text-align:center; margin-top:50px;'>Authentication Failure: Invalid Parameters</h1>", 401

        # Global Control System Form
        elif 'global_update' in request.form:
            if not session.get('logged_in'):
                return "Unauthorized Action", 403
                
            # Content Parsing Loops
            site_data["name"] = request.form.get('name')
            site_data["title"] = request.form.get('title')
            site_data["bio"] = request.form.get('bio')
            site_data["badges"] = [b.strip() for b in request.form.get('badges').split(',') if b.strip()]
            
            site_data["milestones"] = [m.strip() for m in request.form.get('milestones').split('\n') if m.strip()]
            
            site_data["repo_title_1"] = request.form.get('repo_title_1')
            site_data["repo_desc_1"] = request.form.get('repo_desc_1')
            site_data["repo_title_2"] = request.form.get('repo_title_2')
            site_data["repo_desc_2"] = request.form.get('repo_desc_2')
            
            site_data["metric_1"] = request.form.get('metric_1')
            site_data["metric_2"] = request.form.get('metric_2')
            site_data["metric_3"] = request.form.get('metric_3')
            site_data["metric_4"] = request.form.get('metric_4')
            
            site_data["skill_py"] = int(request.form.get('skill_py', 0))
            site_data["skill_flask"] = int(request.form.get('skill_flask', 0))
            site_data["skill_html"] = int(request.form.get('skill_html', 0))
            site_data["skill_css"] = int(request.form.get('skill_css', 0))
            site_data["skill_git"] = int(request.form.get('skill_git', 0))

            save_site_data(site_data)
            return redirect(url_for('index'))

    # Render login screen if unauthenticated
    if not session.get('logged_in'):
        return render_template('admin_login.html')
        
    return render_template('admin.html', data=site_data)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)