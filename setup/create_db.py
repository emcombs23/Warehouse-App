#!/usr/bin/env python3
"""Create a single-table SQLite database for a sports warehouse inventory.

Creates `warehouse_inventory.db` in the workspace root and inserts sample rows.
"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / 'warehouse_inventory.db'

SCHEMA = '''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT,
    size TEXT,
    color TEXT,
    quantity INTEGER NOT NULL DEFAULT 0,
    location TEXT,
    supplier TEXT,
    cost REAL,
    price REAL,
    received_date TEXT,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
'''

SAMPLE_DATA = [
    (
        'SKU-0001', 'Soccer Ball - Pro', 'Balls', '5', 'White/Black', 120,
        'A1', 'SportCo', 12.50, 24.99, '2025-11-01', 'Top seller'
    ),
    (
        'SKU-0002', 'Basketball - Indoor', 'Balls', '7', 'Orange', 80,
        'A2', 'HoopGear', 10.00, 19.99, '2025-12-10', ''
    ),
    (
        'SKU-0003', 'Tennis Racket - Starter', 'Rackets', '4 1/2', 'Blue', 40,
        'B1', 'RacketWorld', 35.0, 69.99, '2026-01-05', 'Bundle pack'
    ),
]


def create_db(path: Path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript(SCHEMA)

    insert_sql = (
        'INSERT OR IGNORE INTO inventory '
        '(sku, name, category, size, color, quantity, location, supplier, cost, price, received_date, notes) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    )

    cur.executemany(insert_sql, SAMPLE_DATA)
    conn.commit()

    cur.execute('SELECT COUNT(*) FROM inventory;')
    count = cur.fetchone()[0]
    conn.close()
    return count


def main():
    created = create_db(DB_PATH)
    print(f'Created/updated database at: {DB_PATH}')
    print(f'Rows in `inventory` table: {created}')
    print('You can inspect the DB with: sqlite3', DB_PATH)


if __name__ == '__main__':
    main()
