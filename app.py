from pydantic import BaseModel, field_validator, ValidationError
from flask import session, Flask, render_template, request, redirect, url_for
from flask.logging import default_handler
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

class StockModel(BaseModel):
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @field_validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()
    
app.logger.removeHandler(default_handler)

file_handler = RotatingFileHandler('flask-stock-portfolio.log', maxBytes=16384, backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('Starting the Flask Stock Portfolio App...')



from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import escape
import secrets

app.secret_key = secrets.token_hex()


@app.route('/')
def index():
    app.logger.info('Calling the index() function.') 
    return render_template('index.html')


@app.route('/about')
def about():
    # return render_template('about.html', company_name="TestDriven.io")
    flash('Thanks for being a user!', 'info')
    return render_template('about.html', company_name='Saif Alvi')

@app.route('/stocks/')
def list_stocks():
    return render_template('stocks.html')

@app.route('/hello/<message>')
def hello_message(message):
    return f'<h1>Welcome {escape(message)}!</h1>'

@app.route('/blogposts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}...</h1>'

@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f'{key}: {value}')
        try:
            stock_data = StockModel(stock_symbol = request.form['stock_symbol'], number_of_shares=request.form['number_of_shares'], purchase_price=request.form['purchase_price'])
            print(stock_data)

            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price
            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')

            app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")


            return redirect(url_for('list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('add_stock.html')