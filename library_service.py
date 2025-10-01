"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count, get_patron_borrowed_books,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    # ADDED: CHECK IF ISBN IS STRING 
    if isbn.isdigit() is False:
        return False, "ISBN must be 13 digits not characters"
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    TODO: Implement R4 as per requirements
    """
    
    # check if book id exists
    if get_book_by_id(book_id) is None:
        return False, "Book ID not found"
    
    # check if patron has borrowed any books
    if get_patron_borrow_count(patron_id) == 0:
        return False, "Patron ID has not borrowed any books"
    
    # check if patron has borrowed the specific book
    borrow = False
    borrowed_books = get_patron_borrowed_books(patron_id)
    for book in borrowed_books:
        if book['book_id'] == book_id:
            # calculate and display late fees owned
            late_fees = calculate_late_fee_for_book(patron_id, book_id)
            # update available copies count
            update_book_availability(book_id, 1)
            # record return date
            update_borrow_record_return_date(patron_id, book_id, datetime.now())
            
            
            return True, (
                f'Book "{book["title"]}" has been returned. '
                f'Late fee: ${late_fees["fee_amount"]:.2f}, '
                f'Days overdue: {late_fees["days_overdue"]}, '
                f'status: {late_fees['status']}'
            )
    
    return False, f'Patron has not borrowed book {book_id}'
            
        
    
    
   # return False, "Book return functionality is not yet implemented."

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 
    
    
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """
    
    
    books_borrowed = get_patron_borrowed_books(patron_id)
    for book in books_borrowed:
        if book['book_id'] == book_id:
            # check if overdue
            if book['is_overdue'] is True:
                # calculate late fee
                borrow_date = book['borrow_date']
                due_date = book['due_date'] 
                # days overdue
                now = datetime.now()
                days_over = (now - due_date).days
                
                if days_over <= 7:
                    fee = days_over * 0.50
                else:
                    fee = (7 * 0.50) +((days_over-7) * 1.00)
                
                fee = min(fee, 15.00)
                
                return {
                    'fee_amount': fee,
                    'days_overdue': days_over,
                    'status': 'over_due'
                }
                
            return {
                    'fee_amount': 0,
                    'days_overdue': 0,
                    'status': 'not_overdue'
                }
            


def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    
    TODO: Implement R6 as per requirements
    """
    
    return []

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """
    return {}
