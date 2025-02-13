import os
import pytest
from project import create_app
from flask import current_app  
from project.models import Stock
from project import database


@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig' # set testing config
    flask_app = create_app()

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
    stock = Stock('AAPL', '16', '406.78')
    return stock

