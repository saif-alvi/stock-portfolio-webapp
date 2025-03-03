from project import database
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import mapped_column
from project import database
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

class Stock(database.Model):
    """
    Class that represents a purchased stock in a portfolio.

    The following attributes of a stock are stored in this table:
        stock symbol (type: string)
        number of shares (type: integer)
        purchase price (type: integer)

    Note: Due to a limitation in the data types supported by SQLite, the
          purchase price is stored as an integer:
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
    
    user_relationship = relationship('User', back_populates='stocks_relationship')  

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str, user_id: str, purchase_date=None):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)
        self.user_id = user_id
        self.purchase_date = purchase_date

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} shares purchased at ${self.purchase_price / 100}'
    


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
    

