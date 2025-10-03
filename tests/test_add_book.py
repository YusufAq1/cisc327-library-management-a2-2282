import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to Python path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_service import add_book_to_catalog

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    with patch('library_service.get_book_by_isbn') as mock_get_book, \
         patch('library_service.insert_book') as mock_insert:
        
        # Mock the database responses
        mock_get_book.return_value = None  # No existing book
        mock_insert.return_value = True    # Insert successful
        
        success, message = add_book_to_catalog("Book98", "TAuthor", "1234567890123", 65)
        
        assert success == True
        assert "successfully added" in message.lower()
        mock_get_book.assert_called_once_with("1234567890123")
        mock_insert.assert_called_once_with("Book98", "TAuthor", "1234567890123", 65, 65)

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Book4", "Test Author", "683026192", 7)
    
    assert success == False
    assert "exactly 13 digits" in message.lower()
    
def test_add_book_invalid_copy():
    """Test adding a book with invalid number of copies."""
    success, message = add_book_to_catalog("Book7", "Test Author", "1234567890123", 0)
    
    assert success == False
    assert "positive integer" in message.lower()
    
def test_add_book_invalid_isbn_with_chars():
    """Test adding a book with invalid isbn containing characters"""
    success, message = add_book_to_catalog("Book 1", "Test Author", "12345678--123", 1)
    
    assert success == False
    assert "must be 13 digits not characters" in message.lower()

def test_add_book_duplicate_isbn():
    """Test adding a book with duplicate ISBN."""
    with patch('library_service.get_book_by_isbn') as mock_get_book:
        # Mock that a book already exists with this ISBN
        mock_get_book.return_value = {"title": "Existing Book", "isbn": "1234567890123"}
        
        success, message = add_book_to_catalog("New Book", "New Author", "1234567890123", 5)
        
        assert success == False
        assert "already exists" in message.lower()

def test_add_book_empty_title():
    """Test adding a book with empty title."""
    success, message = add_book_to_catalog("", "Test Author", "1234567890123", 1)
    
    assert success == False
    assert "title is required" in message.lower()

def test_add_book_title_too_long():
    """Test adding a book with title exceeding 200 characters."""
    long_title = "A" * 201
    success, message = add_book_to_catalog(long_title, "Test Author", "1234567890123", 1)
    
    assert success == False
    assert "title must be less than 200 characters" in message.lower()