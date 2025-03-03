'''
this file test_models.py contains unit tests for models.py file.
'''

from project.models import Stock

def test_new_stock(new_stock):
    """
    GIVEN a Stock model
    WHEN a new Stock object is made
    THEN check the symbol, number of shares, and purchase price fields are defined correctly 
    
    """

    assert new_stock.stock_symbol == 'AAPL'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678
    assert new_stock.user_id == 17
    assert new_stock.purchase_date.year == 2020
    assert new_stock.purchase_date.month == 7
    assert new_stock.purchase_date.day == 18

def test_new_user(new_user):
    """
    Given a User Model
    When a new User object is created
    Then check the email is valid and hashed password does not eqaul the password provied
    """

    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsAwesome123'


def test_set_password(new_user):
    """
    GIVEN a User model
    WHEN the user's password is changed
    THEN check the password has been changed
    """
    new_user.set_password('FlaskIsStillAwesome456')
    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsStillAwesome456'
    assert new_user.is_password_correct('FlaskIsStillAwesome456')
