import os
import pytest
from project import create_app
from flask import current_app  
from project.models import Stock
from project import database
from project.models import Stock, User
from datetime import datetime

@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig' # set testing config
    flask_app = create_app()
    flask_app.extensions['mail'].suppress = True  # NEW!!

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger
        with flask_app.app_context():
            current_app.logger.info('In the test_client() fixture...')

            database.create_all() # create database and tables

        yield testing_client  # this is where the testing happens!

        with flask_app.app_context():
            database.drop_all()

@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78', 17, datetime(2020, 7, 18))
    return stock

@pytest.fixture(scope='module')
def new_user():
    user = User('patrick@email.com', 'FlaskIsAwesome123')
    return user



@pytest.fixture(scope='module')
def register_default_user(test_client):
    # Register the default user
    test_client.post('/users/register',
                     data={'email': 'patrick@gmail.com',
                           'password': 'FlaskIsAwesome123'},
                     follow_redirects=True)
    return

@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    # Log in the default user
    test_client.post('/users/login',
                     data={'email': 'patrick@gmail.com',
                           'password': 'FlaskIsAwesome123'},
                     follow_redirects=True)

    yield   # this is where the testing happens!

    # Log out the default user
    test_client.get('/users/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def confirm_email_default_user(test_client, log_in_default_user):
    # Mark the user as having their email address confirmed
    query = database.select(User).where(User.email == 'patrick@gmail.com')
    user = database.session.execute(query).scalar_one()
    user.email_confirmed = True
    user.email_confirmed_on = datetime(2020, 7, 8)
    database.session.add(user)
    database.session.commit()

    yield user  # this is where the testing happens!

    # Mark the user as not having their email address confirmed (clean up)
    query = database.select(User).where(User.email == 'patrick@gmail.com')
    user = database.session.execute(query).scalar_one()
    user.email_confirmed = False
    user.email_confirmed_on = None
    database.session.add(user)
    database.session.commit()


@pytest.fixture(scope='function')
def afterwards_reset_default_user_password():
    yield  # this is where the testing happens!

    # Since a test using this fixture could change the password for the default user,
    # reset the password back to the default password
    query = database.select(User).where(User.email == 'patrick@gmail.com')
    user = database.session.execute(query).scalar_one()
    user.set_password('FlaskIsAwesome123')
    database.session.add(user)
    database.session.commit()


@pytest.fixture(scope='function')
def add_stocks_for_default_user(test_client, log_in_default_user):
    # Add three stocks for the default user
    test_client.post('/add_stock', data={'stock_symbol': 'SAM',
                                         'number_of_shares': '27',
                                         'purchase_price': '301.23',
                                         'purchase_date': '2020-07-01'})
    test_client.post('/add_stock', data={'stock_symbol': 'COST',
                                         'number_of_shares': '76',
                                         'purchase_price': '14.67',
                                         'purchase_date': '2019-05-26'})
    test_client.post('/add_stock', data={'stock_symbol': 'TWTR',
                                         'number_of_shares': '146',
                                         'purchase_price': '34.56',
                                         'purchase_date': '2020-02-03'})
    return