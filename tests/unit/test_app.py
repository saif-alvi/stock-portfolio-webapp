from pydantic import ValidationError
import pytest
"""
Unit tests for app.py

"""
from app import StockModel


def test_validate_stock_data_nominal():
    """
    Given: A StockModel instance with valid data
    When: The data is valid and passed in
    Then: make sure that validation is successful
    
    """

    stock_data = StockModel(stock_symbol='AAPL', number_of_shares=10, purchase_price=100.0)

    assert stock_data.stock_symbol == 'AAPL'
    assert stock_data.number_of_shares == 10
    assert stock_data.purchase_price == 100.0

def test_validate_stock_data_invalid_stock_symbol():
    """
    Given: A StockModel instance with invalid stock symbol
    When: The stock symbol is invalid
    Then: make sure that validation fails
    
    """

    with pytest.raises(ValueError):
        StockModel(stock_symbol='AAPLL32', number_of_shares=10, purchase_price=66.76)
        
def test_validate_stock_data_invalid_number_of_shares():
    """
    GIVEN a helper class to validate the form data
    WHEN invalid data (invalid number of shares) is passed in
    THEN check that the validation raises a ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel(
            stock_symbol='SBUX',
            number_of_shares='100.1231',  # Invalid!
            purchase_price='45.67'
        )


def test_validate_stock_data_invalid_purchase_price():
    """
    GIVEN a helper class to validate the form data
    WHEN invalid data (invalid purchase price) is passed in
    THEN check that the validation raises a ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel(
            stock_symbol='SBUX',
            number_of_shares='100',
            purchase_price='45,67'  # Invalid!
        )


def test_validate_stock_data_missing_inputs():
    """
    GIVEN a helper class to validate the form data
    WHEN invalid data (missing input) is passed in
    THEN check that the validation raises a ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel()  # Missing input data!


def test_validate_stock_data_missing_purchase_price():
    """
    GIVEN a helper class to validate the form data
    WHEN invalid data (missing purchase price) is passed in
    THEN check that the validation raises a ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel(
            stock_symbol='SBUX',
            number_of_shares='100',
            # Missing purchase_price!
        )