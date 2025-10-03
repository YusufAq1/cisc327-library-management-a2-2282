# tests/conftest.py
import pytest
import sqlite3
import library_service

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    """Setup in-memory database for each test."""
    # Create in-memory SQLite DB
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
    conn.commit()

    # Patch library_service.get_db_connection to use this in-memory DB
    monkeypatch.setattr(library_service, "get_db_connection", lambda: conn)

    yield  # run the test

    conn.close()
