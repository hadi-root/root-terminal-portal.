import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "root_super_secure_vault_key"

DATA_FILE = "site_data.json"

# Safe default dataset structure to prevent 500 template rendering crashes
DEFAULT_DATA = {
    "name": "Hadi",
    "title": "Python Developer | Flask Developer | Future Software Engineer",
    "bio": "Hi, I'm Hadi, a Class 11 student passionate about Python programming, automation, Flask development, and software engineering.",
    "badges": ["Python 3.x", "Flask Framework", "Automation", "Git"],
    "milestones": [
        "Class 11 CBSE Computer Science Track: Actively mastering fundamental computational thinking.",
        "Backend Web Infrastructure Core: Constructed synchronous routing networks using Flask.",
        "Open Source Architecture: Tracking codebase modifications with Git."
    ],
    "repo_title_1": "root-terminal-portal",
    "repo_desc_1": "The production source code for this portfolio interface.",
    "repo_title_2": "python-script-registry",
    "repo_desc_2": "A unified compilation directory storing standard native utilities.",
    "metric_1": "SQLite Database",
    "metric_2": "Interpreter Backbone",
    "metric_3": "Server Architecture",
    "metric_4": "Pipeline Status",
    "skill_py": 90,
    "skill_flask": 80,
    "skill_html": 75,
    "skill_css": 75,
    "skill_git": 60
}

def load_site_data():
    if not os.path.exists(DATA_FILE):
        save_site_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure essential keys exist
            for key, val in DEFAULT_DATA.items():
                if key not in data:
                    data[key] = val
            return data
    except Exception:
        return DEFAULT_DATA

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

    if not session.get('logged_in'):
        return render_template('admin_login.html')
        
    return render_template('admin.html', data=site_data)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)