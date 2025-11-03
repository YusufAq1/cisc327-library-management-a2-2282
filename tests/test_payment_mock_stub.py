from services.payment_service import PaymentGateway
from unittest.mock import Mock
from services.library_service import pay_late_fees
from services.library_service import refund_late_fee_payment
import pytest

# Stubbing 
@pytest.fixture
def stub_late_fee_and_book(mocker):
    
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 10.00, "days_overdue": 3}
    )
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"title": "TestBook"}  
    )
    

# Pay late fees testing 

# Test 1: successfull payment 

def test_pay_late_fees_successful(stub_late_fee_and_book, mocker):
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Approved")
    success, message, txn = pay_late_fees("123456", 1, mock_gateway)
    
    assert success is True
    assert txn == "txn_123"
    assert "successful" in message.lower()
    
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=10.00,
        description="Late fees for 'TestBook'"
    )
    
# Test 2: payment declined 

def test_pay_late_fees_declined(stub_late_fee_and_book):
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, None, "Declined")
    success, message, txn = pay_late_fees("123456", 1, mock_gateway)
    
    assert success is False
    assert txn == None
    assert "failed" in message.lower()
    
    mock_gateway.process_payment.assert_called_once()

# Test 3: imvalid patron 

def test_pay_late_fees_invalid_patron(mocker):
    
    
    mocker.patch("services.library_service.calculate_late_fee_for_book")
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, txn = pay_late_fees("123", 1, mock_gateway)
    
    assert success is False
    assert "invalid patron" in message.lower()
    
    mock_gateway.process_payment.assert_not_called()
    

# Test 4: 0 late fees

def test_pay_late_fees_no_late_fees(mocker):
    
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 0.00, "days_overdue": 0}
    )
   
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, txn = pay_late_fees("123456", 1, mock_gateway)
    
    assert success is False
    assert txn is None
    assert "no late fees to pay for this book" in message.lower()
    
    mock_gateway.process_payment.assert_not_called()
    
# Test 5: network error exception handling

def test_pay_late_fees_network_error(stub_late_fee_and_book):
    
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network Down")
    success, message, txn = pay_late_fees("123456", 1, mock_gateway)
    
    assert success is False
    assert txn is None
    assert "error" in message.lower()
    
    mock_gateway.process_payment.assert_called_once()
    
    

# ADDED FOR COVERAGE 
# Test 6: invalid amount exceeds limit 

def test_pay_late_fees_invalid_amount_exceeds(mocker):
    
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 10.00, "days_overdue": 3}
    )
    
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, txn = pay_late_fees("123456", 9999, mock_gateway)
    
    assert success is False
    assert txn is None
    assert "book not found" in message.lower()
    
    mock_gateway.process_payment.assert_not_called()
    
# test 7: none return value
def test_pay_late_fees_error(mocker):

    mocker.patch(
            'services.library_service.calculate_late_fee_for_book',
            return_value=None  
        )
    
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, txn = pay_late_fees("123456", 1, mock_gateway)
    
    assert success is False
    assert 'Unable to calculate late fees' in message
    assert txn is None
    
    mock_gateway.process_payment.assert_not_called()    
    
# Test 8: invalid amount
def test_pay_late_fee_invalid(mocker):
    
    mocker.patch(
        "services.payment_service.PaymentGateway.process_payment",
        return_value=(False, "", "Invalid amount")
    )

    gateway = PaymentGateway()
    success, txn, msg = gateway.process_payment("123456", 0)

    assert success is False
    assert txn == ""
    assert "invalid amount" in msg.lower()
    

# Test 9: invalid patron ID
def test_pay_late_fee_invalid_patron(mocker):
    
    mocker.patch(
        "services.payment_service.PaymentGateway.process_payment",
        return_value=(False, "", "Invalid patron ID")
    )

    gateway = PaymentGateway()
    success, txn, msg = gateway.process_payment("1234", 20.00)

    assert success is False
    assert txn == ""
    assert "invalid patron id" in msg.lower()
    

# test 10: 
    
    
# refund late feepayment testing 

# test 1: successfull refund

def test_refund_late_fee_payment_successfull():
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund Success")
    success, message = refund_late_fee_payment("txn_111", 10.0, mock_gateway)
    
    assert success is True  
    assert "success" in message.lower()
    
    mock_gateway.refund_payment.assert_called_once_with("txn_111", 10.0)
    


# test 2: invalid transaction ID

def test_refund_late_fee_payment_invalid_transaction_id():
    
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("111", 10.0, mock_gateway)
    
    assert success is False  
    assert "invalid transaction id." in message.lower()
    
    mock_gateway.refund_payment.assert_not_called()
    

# test 3: invalid refund amounts (negative)

def test_refund_late_fee_payment_invalid_amounts_negative():
    
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_111", -10.0, mock_gateway)
    
    assert success is False  
    assert "refund amount must be greater than 0." in message.lower()
    
    mock_gateway.refund_payment.assert_not_called()

# test 4: invalid refund amounts (0)

def test_refund_late_fee_payment_invalid_amounts_0():
    
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_111", 0, mock_gateway)
    
    assert success is False  
    assert "refund amount must be greater than 0." in message.lower()
    
    mock_gateway.refund_payment.assert_not_called()
    
# test 5: invalid refund amounts (exceeds max)

def test_refund_late_fee_payment_invalid_amounts_max():
    
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_111", 18, mock_gateway)
    
    assert success is False  
    assert "refund amount exceeds maximum late fee." in message.lower()
    
    mock_gateway.refund_payment.assert_not_called()
    
# ADDED FOR COVERAGE
# test 6: exception thrown
def test_refund_late_fee_payment_exception():
   
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.side_effect = Exception("Gateway offline")

    success, msg = refund_late_fee_payment("txn_999", 10.00, mock_gateway)

    assert success is False
    assert "error" in msg.lower()
    mock_gateway.refund_payment.assert_called_once()
    

