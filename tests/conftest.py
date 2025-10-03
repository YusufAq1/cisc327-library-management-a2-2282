import pytest
from library_service import borrow_book_by_patron, add_book_to_catalog
from database import get_db_connection

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    """Set up in-memory DB and populate test data."""
    import sqlite3
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

    # Patch get_db_connection to use this DB
    import library_service
    monkeypatch.setattr(library_service, "get_db_connection", lambda: conn)

    yield
    conn.close()