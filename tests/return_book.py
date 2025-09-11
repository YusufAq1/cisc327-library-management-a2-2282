import pytest
from library_service import (
    return_book_by_patron
)

def test_return_valid_book():
    """Test return a valid book."""
    success, message = return_book_by_patron("123456", 3)
    
    assert success == True
    assert "successfully returned" in message.lower()
    
def test_return_valid_book2():
    """Test return a valid book."""
    success, message = return_book_by_patron("654321", 1)
    
    assert success == True
    assert "successfully returned" in message.lower()

def test_return_invalid_book():
    """Test return an invalid book."""
    success, message = return_book_by_patron("654321", 0)
    
    assert success == False
    assert "book ID cannot be found" in message.lower()
    
def test_return_invalid_book2():
    """Test return an invalid patron ID book."""
    success, message = return_book_by_patron("54321", 3)
    
    assert success == False
    assert "invalid patron id" in message.lower()