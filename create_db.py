import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="Saikumar278")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Brolichi")
    print("Database 'Brolichi' created or already exists.")
    db.close()
except Exception as e:
    print(f"Error: {e}")
