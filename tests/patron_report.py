import pytest
from library_service import (
    get_patron_status_report
)

def test_patron_report_valid():
    """Test search for valid patron"""
    success, message = get_patron_status_report("123456")
    
    assert success == True
    assert "generated" in message.lower()
    
def test_patron_report_valid2():
    """Test search for valid patron"""
    success, message = get_patron_status_report("654321")
    
    assert success == True
    assert "generated" in message.lower()
    
def test_patron_report_invalid():
    """Test search for valid patron"""
    success, message = get_patron_status_report("12345")
    
    assert success == False
    assert "invalid patron id" in message.lower()

def test_patron_report_invalid2():
    """Test search for valid patron"""
    success, message = get_patron_status_report("78902")
    
    assert success == False
    assert "invalid patron id" in message.lower()