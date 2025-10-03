import pytest
import sqlite3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_database, get_db_connection

def add_sample_data():
    """Add sample data to the database."""
    conn = get_db_connection()
    
    # Clear any existing data
    conn.execute('DELETE FROM borrow_records')
    conn.execute('DELETE FROM books')
    
    # Add sample books
    sample_books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 3, 3),
        ('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 2, 2),
        ('1984', 'George Orwell', '9780451524935', 1, 1),
        ('Pride and Prejudice', 'Jane Austen', '9780141439518', 4, 4),
    ]
    
    for title, author, isbn, total_copies, available_copies in sample_books:
        conn.execute('''
            INSERT INTO books (title, author, isbn, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, isbn, total_copies, available_copies))
    
    conn.commit()
    conn.close()

@pytest.fixture(autouse=True)
def reset_database():
    """Reset database to sample data before each test."""
    import database
    
    # Use in-memory database
    database.DATABASE = ":memory:"
    
    # Initialize fresh database
    init_database()
    
    # Add sample data
    add_sample_data()
    
    yield  # Test runs here
    
    # No cleanup needed for in-memory database - it disappears automatically