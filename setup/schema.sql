-- Schema for a single-table warehouse inventory
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
