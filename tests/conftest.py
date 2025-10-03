import pytest
import sqlite3
import os
import sys

# Add the parent directory to Python path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_service import (
    add_book_to_catalog,
    borrow_book_by_patron,
    return_book_by_patron,
    calculate_late_fee_for_book,
    search_books_in_catalog,
    get_patron_status_report
)
from database import init_database
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

def test_borrow_valid_book():
    success, message = borrow_book_by_patron("123456", 4)
    assert success is True
    assert "successfully borrowed" in message.lower()