import pytest
import sqlite3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_database, get_db_connection

@pytest.fixture(autouse=True)
def setup_database():
    """Set up an in-memory database before each test."""
    import database
    
    # Use in-memory database for tests
    database.DATABASE = ":memory:"
    
    # Reinitialize with in-memory database
    init_database()
    
    # Add minimal test data
    conn = get_db_connection()
    
    # Add one test book that's definitely available
    conn.execute('''
        INSERT INTO books (title, author, isbn, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Test Book', 'Test Author', '1234567890123', 5, 5))
    
    conn.commit()
    conn.close()