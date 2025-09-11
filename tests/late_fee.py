import pytest
from library_service import (
    calculate_late_fee_for_book
)

def test_late_fee_calculate_valid():
    """Test late fee valid"""
    success, message = calculate_late_fee_for_book("123456", 3)
    
    assert success == True
    assert "late fee calculated" in message.lower()
    
def test_late_fee_calculate_valid2():
    """Test late fee valid."""
    success, message = calculate_late_fee_for_book("654321", 1)
    
    assert success == True
    assert "late fee calculated" in message.lower()

def test_late_fee_calculate_invalid():
    """Test late fee for invalid book."""
    success, message = calculate_late_fee_for_book("123456", 0)
    
    assert success == False
    assert "invalid book id" in message.lower()
    
def test_late_fee_calculate_invalid2():
    """Test late fee for invalid patron."""
    success, message = calculate_late_fee_for_book("12345", 3)
    
    assert success == False
    assert "invalid patron id" in message.lower()