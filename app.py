import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "root_secure_key_2026"

DATA_FILE = "site_data.json"

def load_site_data():
    if not os.path.exists(DATA_FILE):
        # Default text parameters safely stored
        default_data = {
            "name": "Hadi",
            "title": "Python Developer | Flask Developer | Future Software Engineer",
            "bio": "Hi, I'm Hadi, a Class 11 CBSE student passionate about Python programming, automation, Flask development, and software engineering. This portfolio showcases my projects and technical skills as I build foundations for enterprise application architecture."
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
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
    ADMIN_PASSWORD = "hadi_secure_pass"  # Master authorization token

    if request.method == 'POST':
        entered_pass = request.form.get('password')
        if entered_pass == ADMIN_PASSWORD:
            site_data["name"] = request.form.get('name')
            site_data["title"] = request.form.get('title')
            site_data["bio"] = request.form.get('bio')
            save_site_data(site_data)
            return redirect(url_for('index'))
        else:
            return "<h1 style='color:#ff3333; font-family:monospace; text-align:center; margin-top:50px;'>Access Denied: Invalid Security Key</h1>", 403
            
    return render_template('admin.html', data=site_data)

if __name__ == "__main__":
    app.run(debug=True)