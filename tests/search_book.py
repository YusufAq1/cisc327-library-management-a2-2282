import pytest
from library_service import (
    search_books_in_catalog
)

def test_search_book_valid():
    """Test search for valid book"""
    success, message = search_books_in_catalog("1984", "title")
    
    assert success == True
    assert "found" in message.lower()
    
def test_search_book_valid2():
    """Test search for valid book"""
    success, message = search_books_in_catalog("9780451524935", "ISBN")
    
    assert success == True
    assert "found" in message.lower()
    
def test_search_book_invalid():
    """Test search for invalid book"""
    success, message = search_books_in_catalog("9780743273500", "ISBN")
    
    assert success == False
    assert "not found" in message.lower()

def test_search_book_invalid2():
    """Test search for invalid book"""
    success, message = search_books_in_catalog("George", "Key")
    
    assert success == False
    assert "not found" in message.lower()