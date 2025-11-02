import pytest
from services.library_service import (
    add_book_to_catalog
)
import random


def test_add_book_valid_input():
    """Test adding a book with valid input."""
    # generate random isbn
    number = random.randint(1111111111111, 9999999999999)
    success, message = add_book_to_catalog("Book98", "TAuthor", str(number), 65)
    
    assert success == True
    assert "successfully added" in message.lower()

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
    
def test_add_book_invalid_isbn():
    """Test adding a book with invalid isbn"""
    success, message = add_book_to_catalog("Book 1", "Test Author", "12345678--123", 0)
    
    assert success == False
    assert "isbn must be 13 digits not characters" in message.lower()