import os
import pytest
from project import create_app
from flask import current_app  
from project.models import Stock


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger
        with flask_app.app_context():
            current_app.logger.info('In the test_client() fixture...')

        yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78')
    return stock