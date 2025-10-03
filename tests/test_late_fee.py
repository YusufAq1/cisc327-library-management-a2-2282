import pytest
from library_service import calculate_late_fee_for_book
from library_service import borrow_book_by_patron

def test_late_fee_valid_overdue():
    
    fee_info = calculate_late_fee_for_book("123456", 1)
    assert isinstance(fee_info, dict)
    assert "fee_amount" in fee_info
    assert "status" in fee_info
    assert fee_info["status"] in ["over_due", "not_overdue"]

def test_late_fee_valid_not_overdue():
    
    
    borrow_book_by_patron("654321", 4)
    fee_info = calculate_late_fee_for_book("654321", 4)
    assert fee_info["fee_amount"] == 0
    assert fee_info["status"] == "not_overdue"

def test_late_fee_invalid_book():
    
    fee_info = calculate_late_fee_for_book("123456", 0)
    
    assert isinstance(fee_info, dict) or fee_info is None

def test_late_fee_invalid_patron():
    
    fee_info = calculate_late_fee_for_book("12345", 3)
    
    assert fee_info is None or fee_info == {}

