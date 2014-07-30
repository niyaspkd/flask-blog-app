import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE blogspot (id integer primary key autoincrement,author text,post text,day text,time text,comment text)''')
conn.commit()
conn.close()
