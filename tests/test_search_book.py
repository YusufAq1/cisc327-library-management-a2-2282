import pytest
from library_service import search_books_in_catalog

    
def test_search_book_valid_by_title():
    results = search_books_in_catalog("1984", "title")
    assert isinstance(results, list)
    assert any("1984" in book["title"].lower() for book in results)

def test_search_book_valid_by_isbn():
    
    results = search_books_in_catalog("9780451524935", "isbn")
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["title"] == "1984"

def test_search_book_invalid_isbn():
    
    results = search_books_in_catalog("8242725497725", "isbn")
    assert results == [None]  

def test_search_book_invalid_type():
    
    results = search_books_in_catalog("George", "key")
    assert results == [] 

def test_search_books_by_author():
    """Test search for books by author."""
    results = search_books_in_catalog("George Orwell", "author")
    assert isinstance(results, list)
    assert any("Orwell" in book["author"] for book in results)

def test_search_books_case_insensitive():
    
    results = search_books_in_catalog("george orwell", "author")
    assert isinstance(results, list)
    assert any("Orwell" in book["author"] for book in results)
