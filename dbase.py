import sqlite3
import os

conn = sqlite3.connect('stockindia.db')
c = conn.cursor()
print("[DEBUG] database file location:", os.path.abspath('stockindia.db'))
# sqlite3 "C:\python\Python 3.13\PycharmProjects\mynseproject\stockindia\stockindia.db" (python db path)



c.execute('''
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    open_price REAL NOT NULL,
    close_price REAL NOT NULL,
    ltp REAL NOT NULL,
    change REAL NOT NULL,
    volume INT NOT NULL
)''')

c.execute('''
CREATE TABLE IF NOT EXISTS stocks_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    company_name TEXT NOT NULL,
    open_price REAL NOT NULL,
    close_price REAL NOT NULL,
    ltp REAL NOT NULL,
    change REAL NOT NULL,
    volume INT NOT NULL
)''')

conn.commit()
