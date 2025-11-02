import pytest
from services.library_service import get_patron_status_report

def test_patron_report_valid():
    
    report = get_patron_status_report("012345")
    assert report["success"] == True
    assert "borrow_count" in report["data"]
    assert "patron 012345" in report["message"].lower()

def test_patron_report_valid2():
  
    report = get_patron_status_report("654321")
    assert report["success"] == True
    assert "borrow_count" in report["data"]

def test_patron_report_invalid_short_id():
    
    report = get_patron_status_report("12345")  
    assert report["success"] == False
    assert "invalid patron id" in report["message"].lower()

def test_patron_report_invalid_non_digit():
    
    report = get_patron_status_report("78a902")  
    assert report["success"] == False
    assert "invalid patron id" in report["message"].lower()

