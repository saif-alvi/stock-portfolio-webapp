from project import database
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import mapped_column
from project import database
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from flask import current_app
import requests

#------------HELPER------------------

def create_alpha_vantage_url_quote(symbol: str) -> str:
    return 'https://www.alphavantage.co/query?function={}&symbol={}&apikey={}'.format(
        'GLOBAL_QUOTE',
        symbol,
        current_app.config['ALPHA_VANTAGE_API_KEY']
    )

def get_current_stock_price(symbol: str) -> float:
    url = create_alpha_vantage_url_quote(symbol)

    # Attempt the GET call to Alpha Vantage and check that a ConnectionError does
    # not occur, which happens when the GET call fails due to a network issue
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        current_app.logger.error(
            f'Error! Network problem preventing retrieving the stock data ({symbol})!')

    # Status code returned from Alpha Vantage needs to be 200 (OK) to process stock data
    if r.status_code != 200:
        current_app.logger.warning(f'Error! Received unexpected status code ({r.status_code}) '
                                   f'when retrieving daily stock data ({symbol})!')
        return 0.0

    stock_data = r.json()

    # The key of 'Global Quote' needs to be present in order to process the stock data.
    # Typically, this key will not be present if the API rate limit has been exceeded.
    if 'Global Quote' not in stock_data:
        current_app.logger.warning(f'Could not find the Global Quote key when retrieving '
                                   f'the daily stock data ({symbol})!')
        return 0.0

    return float(stock_data['Global Quote']['05. price'])




#------------HELPER------------------


class Stock(database.Model):
    """
    Class that represents a purchased stock in a portfolio

    The following attributes of a stock are stored in this table:
        stock symbol (type: string)
        number of shares (type: integer)
        purchase price (type: integer)
        primary key of User that owns the stock (type: integer)
        purchase date (type: datetime)
        current price (type: integer)
        date when current price was retrieved from the Alpha Vantage API (type: datetime)
        position value = current price * number of shares (type: integer)

    Note: Due to a limitation in the data types supported by SQLite, the
          purchase price, current price, and position value are stored as integers:
              $24.10 -> 2410
              $100.00 -> 10000
              $87.65 -> 8765
    """

    __tablename__ = 'stocks'

    id = mapped_column(Integer(), primary_key=True)
    stock_symbol = mapped_column(String())
    number_of_shares = mapped_column(Integer())
    purchase_price = mapped_column(Integer())
    user_id = mapped_column(ForeignKey('users.id'))
    purchase_date = mapped_column(DateTime())
    current_price = mapped_column(Integer())       
    current_price_date = mapped_column(DateTime())  
    position_value = mapped_column(Integer())
    
    user_relationship = relationship('User', back_populates='stocks_relationship')  

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str, user_id: str, purchase_date=None):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)
        self.user_id = user_id
        self.purchase_date = purchase_date
        self.current_price = 0          
        self.current_price_date = None  
        self.position_value = 0        

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} shares purchased at ${self.purchase_price / 100}'
    
    def get_stock_data(self):
        if self.current_price_date is None or self.current_price_date.date() != datetime.now().date():
            current_price = get_current_stock_price(self.stock_symbol)
            if current_price > 0.0:
                self.current_price = int(current_price * 100)
                self.current_price_date = datetime.now()
                self.position_value = self.current_price * self.number_of_shares
                current_app.logger.debug(f'Retrieved current price {self.current_price / 100} '
                                        f'for the stock data ({self.stock_symbol})!')
    def get_stock_position_value(self) -> float:
        return float(self.position_value / 100)

class User(flask_login.UserMixin, database.Model):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)

    REMEMBER: Never store the plaintext password in a database!
    """
    __tablename__ = 'users'

    id = mapped_column(Integer(), primary_key=True)
    email = mapped_column(String(), unique=True)
    password_hashed = mapped_column(String(128))
    registered_on = mapped_column(DateTime())                 
    email_confirmation_sent_on = mapped_column(DateTime())     
    email_confirmed = mapped_column(Boolean(), default=False)  
    email_confirmed_on = mapped_column(DateTime())

    stocks_relationship = relationship('Stock', back_populates='user_relationship')

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = datetime.now()
        self.email_confirmed = False
        self.email_confirmed_on = None

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'
    
    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)
    



