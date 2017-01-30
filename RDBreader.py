import sqlite3
conn = sqlite3.connect("systeminfo.db")

 

def read_from_db():
    cur.execute('SELECT * FROM systeminfo')
    data = cur.fetchall()
    for row in data:
        print(row)


cur = conn.cursor()

results = cur.fetchall()
print(results)