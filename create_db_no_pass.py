import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Brolichi")
    print("Database 'Brolichi' created or already exists (No password).")
    db.close()
except Exception as e:
    print(f"Error: {e}")
