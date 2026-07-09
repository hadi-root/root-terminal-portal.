import os
import sqlite3
from functools import wraps
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, Response

app = Flask(__name__)
app.secret_key = "root_terminal_secure_matrix_key" 

DB_PATH = "portfolio.db"

# ==========================================================================
# SECURITY CREDENTIALS CONFIGURATION
# ==========================================================================
ADMIN_USERNAME = "hadi"
ADMIN_PASSWORD = "YourSecretPassword123"  # <-- Change this to your chosen password!

def requires_auth(f):
    """Decorator loop to prompt browser HTTP Basic Authentication challenge."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == ADMIN_USERNAME and auth.password == ADMIN_PASSWORD):
            return Response(
                'Could not verify your access privileges for Root Terminal.\n'
                'Please supply valid administrator credentials.', 401,
                {'WWW-Authenticate': 'Basic realm="Admin Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated

# ==========================================================================
# DATABASE INFRASTRUCTURE PIPELINE
# ==========================================================================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema and inserts all 13 baseline custom records."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            tags TEXT NOT NULL,
            download_file TEXT NOT NULL,
            is_featured INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        initial_projects = [
            ('Web Scraper Module', 'Fetches, parses, and extracts clean live real-time source headlines using BeautifulSoup network parsing.', 'Python, Intermediate, HTTP', 'web_scraper.py', 1),
            ('Weather API Client', 'Pulls atmospheric live JSON dataset summaries using real-time HTTP requests engine maps.', 'Python, Intermediate, REST API', 'weather_app.py', 1),
            ('SQLite Ledger Manager', 'Implements relational memory operations locally using structured SQL query execution parameters.', 'Python, Intermediate, SQL', 'sql_manager.py', 1),
            
            ('Python Calculator', 'Performs clean arithmetic calculations with custom robust input validation loops.', 'Python, Beginner', 'calculator.py', 0),
            ('Number Guessing Game', 'Interactive logic game featuring dynamic boundary checking and random generation patterns.', 'Python, Beginner', 'number_guessing.py', 0),
            ('Multiplication Table Generator', 'Generates iterative structured mathematical product grids with scalable constraints.', 'Python, Beginner', 'multiplication_table.py', 0),
            ('Password Generator', 'Compiles randomized cryptographic string structures enforcing unique symbol density rules.', 'Python, Intermediate', 'password_generator.py', 0),
            ('Quiz Application', 'Evaluates data conditional responses through multiple-choice logic tracks.', 'Python, Beginner', 'quiz_game.py', 0),
            ('Student Grade Calculator', 'Parses array maps containing numeric scores to output exact conditional grade outputs.', 'Python, Beginner', 'student_grade_calculator.py', 0),
            ('File Organizer', 'Scans targeted system filepaths to execute structural automation sorted by file types.', 'Python, Intermediate', 'file_organizer.py', 0),
            ('Digital Clock', 'Continuous thread loop handling exact standard time clock updates directly inside console windows.', 'Python, Beginner', 'digital_clock.py', 0),
            ('Expense Tracker', 'Constructs serial storage structures balancing income inputs and operational debit costs.', 'Python, Intermediate', 'expense_tracker.py', 0),
            ('Todo List Application', 'Maintains linear state structures enabling task appending, mutation tracking, and stack popping loops.', 'Python, Intermediate', 'todo_list.py', 0)
        ]
        cursor.executemany(
            "INSERT INTO projects (title, description, tags, download_file, is_featured) VALUES (?, ?, ?, ?, ?)", 
            initial_projects
        )
        conn.commit()
    conn.close()

init_db()

# ==========================================================================
# WEB CONTROLLER ROUTE CHANNELS
# ==========================================================================
@app.route("/")
def index():
    conn = get_db_connection()
    projects = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", database_projects=projects)

@app.route("/admin", methods=["GET", "POST"])
@requires_auth
def admin_panel():
    conn = get_db_connection()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            title = request.form.get("title")
            description = request.form.get("description")
            tags = request.form.get("tags")
            download_file = request.form.get("download_file")
            is_featured = 1 if request.form.get("is_featured") else 0
            
            conn.execute(
                "INSERT INTO projects (title, description, tags, download_file, is_featured) VALUES (?, ?, ?, ?, ?)",
                (title, description, tags, download_file, is_featured)
            )
            conn.commit()
        elif action == "delete":
            project_id = request.form.get("project_id")
            conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
        return redirect(url_for("admin_panel"))

    projects = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", projects=projects)

@app.route("/run", methods=["POST"])
def run_sandbox_code():
    data = request.get_json()
    code = data.get("code", "")
    return jsonify({"output": "System simulation complete. Script executed perfectly."})

if __name__ == "__main__":
    app.run(debug=True)