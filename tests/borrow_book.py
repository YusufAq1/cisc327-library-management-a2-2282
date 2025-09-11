import pytest
from library_service import (
    borrow_book_by_patron
)

def test_borrow_valid_book():
    """Test borrow a valid book."""
    success, message = borrow_book_by_patron("123456", 3)
    
    assert success == True
    assert "successfully borrowed" in message.lower()

def test_borrow_invalid_book():
    """Test borrow an invalid book id."""
    success, message = borrow_book_by_patron("123456", 0)
    
    assert success == False
    assert "invalid book id" in message.lower()
    
def test_borrow_invalid_patron():
    """Test borrow an invalid patron id."""
    success, message = borrow_book_by_patron("1234567", 3)
    
    assert success == False
    assert "invalid patron id" in message.lower()

def test_borrow_valid():
    """Test borrow an valid book."""
    success, message = borrow_book_by_patron("654321", 3)
    
    assert success == True
    assert "successfully borrowed" in message.lower()