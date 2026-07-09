import sqlite3

def initialize_ledger():
    print("[+] Connecting to local storage ledger database engine...")
    connection = sqlite3.connect(":memory:") # Creates transient database in RAM memory
    cursor = connection.cursor()
    
    # Establish structural schema mapping
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_name TEXT NOT NULL,
            allocation_count INTEGER DEFAULT 0
        )
    ''')
    
    # Run structured transaction inserts
    print("[+] Executing data allocation transactions...")
    modules = [('Web Scraper Package', 120), ('API Client Terminal', 85), ('SQL Ledger Module', 210)]
    cursor.executemany("INSERT INTO inventory (component_name, allocation_count) VALUES (?, ?)", modules)
    connection.commit()
    
    # Parse transaction summary logs
    cursor.execute("SELECT * FROM inventory WHERE allocation_count > 100")
    records = cursor.fetchall()
    
    print("\n[✓] Relational Query Result Set Map:\n" + "="*40)
    for record in records:
        print(f"ID: {record[0]} | Module Node: {record[1]} | Sync Count: {record[2]}")
        
    connection.close()
    print("\n[+] Connection matrix released successfully.")

if __name__ == "__main__":
    initialize_ledger()