#!/usr/bin/env python3
"""Modify the warehouse SQLite DB: remove sqlite_sequence and populate `inventory`.

This script will attempt to drop the `sqlite_sequence` table. If dropping fails
it will delete rows from `sqlite_sequence`. Then it will insert additional
sample rows into the `inventory` table.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'warehouse_inventory.db'

NEW_DATA = [
    ('SKU-0004', 'Baseball Glove - Youth', 'Gloves', 'L', 'Brown', 60, 'C1', 'GripPro', 18.0, 39.99, '2026-02-10', ''),
    ('SKU-0005', 'Running Shoes - Men', 'Footwear', '10', 'Black', 150, 'D3', 'RunFast', 45.0, 89.99, '2026-02-20', ''),
    ('SKU-0006', 'Hockey Stick - Pro', 'Sticks', '60in', 'Black', 30, 'E2', 'IceWorks', 55.0, 129.99, '2026-03-01', 'Limited'),
    ('SKU-0007', 'Yoga Mat - Eco', 'Accessories', 'Standard', 'Green', 200, 'F1', 'ZenGoods', 8.0, 19.99, '2026-03-05', ''),
    ('SKU-0008', 'Swim Goggles - Adult', 'Swim', 'OneSize', 'Clear', 90, 'G4', 'AquaTech', 4.5, 12.99, '2026-03-10', '')
]


def modify_db(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"DB not found: {path}")

    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # Try dropping the sqlite_sequence table outright
    try:
        cur.execute('DROP TABLE IF EXISTS sqlite_sequence;')
        print('Dropped sqlite_sequence (if it existed).')
    except sqlite3.DatabaseError as e:
        print('DROP TABLE failed, attempting to delete rows from sqlite_sequence:', e)
        try:
            cur.execute("DELETE FROM sqlite_sequence;")
            print('Deleted rows from sqlite_sequence.')
        except Exception as e2:
            print('Failed to clear sqlite_sequence:', e2)

    insert_sql = (
        'INSERT OR IGNORE INTO inventory '
        '(sku, name, category, size, color, quantity, location, supplier, cost, price, received_date, notes) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    )

    cur.executemany(insert_sql, NEW_DATA)
    conn.commit()

    cur.execute('SELECT COUNT(*) FROM inventory;')
    count = cur.fetchone()[0]
    conn.close()
    return count


def main():
    count = modify_db(DB_PATH)
    print(f'Inventory rows after modification: {count}')


if __name__ == '__main__':
    main()
