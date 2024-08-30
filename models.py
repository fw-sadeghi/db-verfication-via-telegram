import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('serials.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS serials (
                 id INTEGER PRIMARY KEY,
                 reference_number TEXT,
                 description TEXT,
                 start_serial TEXT,
                 end_serial TEXT,
                 date TEXT)''')
    conn.commit()
    conn.close()

def add_serial(reference_number, description, start_serial, end_serial, date):
    conn = sqlite3.connect('serials.db')
    c = conn.cursor()
    
    # تبدیل تمامی ورودی‌ها به رشته برای جلوگیری از خطای نوع داده
    reference_number = str(reference_number)
    description = str(description)
    start_serial = str(start_serial)
    end_serial = str(end_serial)
    date = str(date)
    
    c.execute('''INSERT INTO serials 
                 (reference_number, description, start_serial, end_serial, date) 
                 VALUES (?, ?, ?, ?, ?)''', 
              (reference_number, description, start_serial, end_serial, date))
    conn.commit()
    conn.close()


def check_serial(serial_number):
    conn = sqlite3.connect('serials.db')
    c = conn.cursor()
    c.execute("SELECT description FROM serials WHERE ? BETWEEN start_serial AND end_serial", (serial_number,))
    result = c.fetchone()
    conn.close()
    return result

def import_from_excel(file_path):
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        add_serial(
            reference_number=row['Reference Number'],
            description=row['Description'],
            start_serial=row['Start Serial'],
            end_serial=row['End Serial'],
            date=row['Date']
        )
def reset_db():
    conn = sqlite3.connect('serials.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS serials")
    conn.commit()
    conn.close()
    init_db()  # جدول را دوباره ایجاد می‌کند
