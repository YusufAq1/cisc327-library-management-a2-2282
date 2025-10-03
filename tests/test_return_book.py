import pytest
from library_service import return_book_by_patron
from library_service import borrow_book_by_patron

def test_return_valid_book():
    
    borrow_book_by_patron("123456", 4)
    success, message = return_book_by_patron("123456", 4)
    assert success == True
    assert "has been returned" in message.lower()

def test_return_valid_book2():
    """Test returning a valid book after borrowing it first."""
    
    
    borrow_book_by_patron("654321", 4)
    success, message = return_book_by_patron("654321", 4)
    assert success == True
    assert "has been returned" in message.lower()

def test_return_invalid_book():
    """Test returning a book that does not exist."""
    success, message = return_book_by_patron("654321", 0)  
    assert success == False
    assert "book id not found" in message.lower()

def test_return_invalid_patron():
    """Test returning with an invalid patron (wrong length ID)."""
    success, message = return_book_by_patron("54321", 3) 
    assert success == False
   
    assert "not borrowed any books" in message.lower()
