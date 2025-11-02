import pytest
from services.library_service import (search_books_in_catalog, add_book_to_catalog)
    
def test_search_book_valid_by_title(): 
    add_book_to_catalog("B1", "yusuf", "9875674324561", 10)
    results = search_books_in_catalog("B1", "title") 
    assert isinstance(results, list) 
    assert any(book["title"].lower() == "b1" for book in results)

    
def test_search_book_valid_by_isbn():
    
    results = search_books_in_catalog("9875674324561", "isbn")
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["title"] == "B1"
    
def test_search_book_invalid_isbn():
    
    results = search_books_in_catalog("8242725497725", "isbn")
    assert results == [None]  
    
def test_search_book_invalid_type():
    
    results = search_books_in_catalog("George", "key")
    assert results == [] 
    
def test_search_books_by_author():
    """Test search for books by author."""
    results = search_books_in_catalog("yusuf", "author")
    assert isinstance(results, list)
    assert any("yusuf" in book["author"] for book in results)
    
