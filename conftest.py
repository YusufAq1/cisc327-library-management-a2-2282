import pytest
import sqlite3
import os
from library_service import (
    add_book_to_catalog
)

@pytest.fixture
def setup_test_db():
    """Set up a test database with required tables."""
    test_db = "test_library.db"
    
    # Remove existing test database
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create connection and tables
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    # Create books table
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            total_copies INTEGER NOT NULL,
            available_copies INTEGER NOT NULL
        )
    ''')
    
    # Create other necessary tables (borrow_records, etc.)
    cursor.execute('''
        CREATE TABLE borrow_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patron_id TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield test_db
    
    # Cleanup
    if os.path.exists(test_db):
        os.remove(test_db)