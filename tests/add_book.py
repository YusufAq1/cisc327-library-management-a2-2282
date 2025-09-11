import pytest
from library_service import (
    add_book_to_catalog
)

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Book 1", "TAuthor", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Book 1", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message
    
def test_add_book_invalid_copy():
    """Test adding a book with invalid number of copies."""
    success, message = add_book_to_catalog("Book 1", "Test Author", "1234567890123", 0)
    
    assert success == False
    assert "must be greater than or equal to 1" in message
    
def test_add_book_invalid_isbn():
    """Test adding a book with invalid isbn"""
    success, message = add_book_to_catalog("Book 1", "Test Author", "12345678--123", 0)
    
    assert success == False
    assert "must contain 13 digits" in message