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
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield test_db
    
    # Cleanup
    if os.path.exists(test_db):
        os.remove(test_db)

@pytest.fixture(autouse=True)
def setup_database():
    """Initialize the database before each test."""
    init_database()