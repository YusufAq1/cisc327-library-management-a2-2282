import pytest
from library_service import (
    borrow_book_by_patron
)

def test_borrow_valid_book():
    
    success, message = borrow_book_by_patron("123456", 1)
    assert success is True
    assert "successfully borrowed" in message.lower()

def test_borrow_invalid_book():
    
    success, message = borrow_book_by_patron("123456", 0)  
    assert success is False
    assert "book not found" in message.lower()

def test_borrow_invalid_patron():
    
    success, message = borrow_book_by_patron("1234567", 1)  
    assert success is False
    assert "invalid patron id" in message.lower()

def test_borrow_unavailable_book():
  
    success, message = borrow_book_by_patron("654321", 3)
    assert success is False
    assert "book not found" in message.lower()
