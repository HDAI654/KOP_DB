import sqlite3
def read(address, tbl):
    conn = sqlite3.connect(str(address))
    cursor = conn.cursor()
    data = list(cursor.execute(f"select * from {str(tbl)}").fetchall())
    conn.commit()
    conn.close()
    return data