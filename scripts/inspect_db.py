import sqlite3

conn = sqlite3.connect('database/agrovision_warehouse.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cursor.fetchall()]
print('Database Tables:', tables)

for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {t};")
    cnt = cursor.fetchone()[0]
    cursor.execute(f"PRAGMA table_info({t});")
    cols = [(c[1], c[2]) for c in cursor.fetchall()]
    cursor.execute(f"PRAGMA foreign_key_list({t});")
    fks = cursor.fetchall()
    print(f"\nTable: {t} ({cnt} rows)")
    print("  Columns:", cols[:8])
    if fks:
        print("  Foreign Keys:", [(fk[2], fk[3], fk[4]) for fk in fks])
