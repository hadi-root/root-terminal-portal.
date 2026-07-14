import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create the key-value configuration table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Default portfolio data matrix
    default_data = {
        "name": "ROOT-TERMINAL-HUB",
        "title": "Python Developer | Flask Developer | Future Software Engineer",
        "bio": "Hi, I'm Hadi, a Class 11 student passionate about Python programming, automation, Flask development, and software engineering.",
        "badges": "Python 3.x, Flask Framework, Automation, Git",
        "milestones": "Class 11 Computer Science Track: Actively mastering fundamental computational thinking.\nBackend Web Infrastructure Core: Constructed synchronous routing networks using Flask.\nOpen Source Architecture: Tracking codebase modifications with Git.",
        "repo_title_1": "root-terminal-portal",
        "repo_desc_1": "The production source code for this portfolio interface.",
        "repo_title_2": "python-script-registry",
        "repo_desc_2": "A unified compilation directory storing standard native utilities.",
        "metric_1": "SQLite Database",
        "metric_2": "Interpreter Backbone",
        "metric_3": "Server Architecture",
        "metric_4": "Pipeline Status",
        "skill_py": "90",
        "skill_flask": "80",
        "skill_html": "75",
        "skill_css": "75",
        "skill_git": "60"
    }
    
    # Insert keys if they don't exist yet
    for key, value in default_data.items():
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
        
    conn.commit()
    conn.close()
    print("Database initialized successfully as database.db!")

if __name__ == '__main__':
    init_db()