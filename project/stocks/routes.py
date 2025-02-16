from . import stocks_blueprint
from flask import current_app, render_template, request, session, flash, redirect, url_for
from pydantic import BaseModel, field_validator, ValidationError
from project.models import Stock
from project import database
import click



@stocks_blueprint.before_request
def stocks_before_request():
    current_app.logger.info('Calling before_request() for the stocks blueprint...')


@stocks_blueprint.after_request
def stocks_after_request(response):
    current_app.logger.info('Calling after_request() for the stocks blueprint...')
    return response


@stocks_blueprint.teardown_request
def stocks_teardown_request(error=None):
    current_app.logger.info('Calling teardown_request() for the stocks blueprint...')

# Helper Class---------------

class StockModel(BaseModel):
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @field_validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()
    
# View Functions----------------

@stocks_blueprint.route('/')
def index():
    current_app.logger.info('Calling the index() function.') 
    return render_template('stocks/index.html')

@stocks_blueprint.route('/stocks/')
def list_stocks():
    query = database.select(Stock).order_by(Stock.id)
    stocks = database.session.execute(query).scalars().all()
    return render_template('stocks/stocks.html', stocks=stocks)

@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f'{key}: {value}')
        try:
            stock_data = StockModel(stock_symbol = request.form['stock_symbol'], number_of_shares=request.form['number_of_shares'], purchase_price=request.form['purchase_price'])
            print(stock_data)

            new_stock = Stock(stock_data.stock_symbol,
            stock_data.number_of_shares,
            stock_data.purchase_price)
            database.session.add(new_stock)
            database.session.commit()


            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')

            current_app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")


            return redirect(url_for('stocks.list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('stocks/add_stock.html')


#------------------CLI COMMANDS-------------------------------------------

@stocks_blueprint.cli.command('create_default_set')
def create_default_set():
    "create 3 new stocks and add to database"
    stock1 = Stock('HD', '25', '247.29')
    stock2 = Stock('TWTR', '230', '31.89')
    stock3 = Stock('DIS', '65', '118.77')
    database.session.add(stock1)
    database.session.add(stock2)
    database.session.add(stock3)
    database.session.commit()

@stocks_blueprint.cli.command('create')
@click.argument('symbol')
@click.argument('number_of_shares')
@click.argument('purchase_price')
def create(symbol, number_of_shares, purchase_price):
    """Create a new stock and add it to the database"""
    stock = Stock(symbol, number_of_shares, purchase_price)
    database.session.add(stock)
    database.session.commit()

