import pytest
import sqlite3
import database  # patch this, not library_service

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            isbn TEXT UNIQUE,
            quantity INTEGER
        )
    ''')
    conn.execute('''
        CREATE TABLE patrons (
            id TEXT PRIMARY KEY,
            name TEXT
        )
    ''')
    # Add test data
    conn.execute("INSERT INTO books (id, title, author, isbn, quantity) VALUES (4, 'Test Book', 'Test Author', '1234567890123', 1)")
    conn.execute("INSERT INTO patrons (id, name) VALUES ('123456', 'Test Patron')")
    conn.commit()

    # Patch the actual database module
    monkeypatch.setattr(database, "get_db_connection", lambda: conn)

    yield
    conn.close()
