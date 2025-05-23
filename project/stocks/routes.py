from . import stocks_blueprint
from flask import current_app, render_template, request, session, flash, redirect, url_for, abort
from pydantic import BaseModel, field_validator, ValidationError
from project.models import Stock
from project import database
import click
from flask_login import login_required, current_user
from datetime import datetime
from textblob import TextBlob
import requests
from flask import render_template, request, redirect, url_for, flash, current_app, abort


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
@login_required
def list_stocks():
    query = database.select(Stock).where(Stock.user_id == current_user.id).order_by(Stock.id)
    stocks = database.session.execute(query).scalars().all()

    current_account_value = 0.0
    for stock in stocks:
        stock.get_stock_data()
        database.session.add(stock)
        current_account_value += stock.get_stock_position_value()

    database.session.commit()
    return render_template('stocks/stocks.html', stocks=stocks, value=round(current_account_value, 2))

@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
@login_required
def add_stock():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f'{key}: {value}')
        try:
            stock_data = StockModel(stock_symbol = request.form['stock_symbol'], number_of_shares=request.form['number_of_shares'], purchase_price=request.form['purchase_price'])
            print(stock_data)

            new_stock = Stock(stock_data.stock_symbol,
                stock_data.number_of_shares,
                stock_data.purchase_price,
                current_user.id,    
                datetime.fromisoformat(request.form['purchase_date']))  
            database.session.add(new_stock)
            database.session.commit()


            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')

            current_app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")


            return redirect(url_for('stocks.list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('stocks/add_stock.html')


@stocks_blueprint.route('/sentiment', methods=['GET', 'POST'])
def stock_sentiment():
    if request.method == 'POST':
        stock_symbol = request.form.get('stock_symbol')
        if not stock_symbol:
            flash("Please enter a stock symbol.", "error")
            return render_template('stocks/sentiment.html')

        # Fetch news headlines using a news API
        api_key = "8d2a9f1f40e44ef4813906d92a3827d9"  # Replace with your NewsAPI key
        url = f"https://newsapi.org/v2/everything?q={stock_symbol}&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            flash("Failed to fetch news. Please try again later.", "error")
            return render_template('stocks/sentiment.html')

        news_data = response.json()
        headlines = [article['title'] for article in news_data.get('articles', [])]

        # Perform sentiment analysis
        sentiment_results = {"positive": 0, "neutral": 0, "negative": 0}
        for headline in headlines:
            analysis = TextBlob(headline)
            if analysis.sentiment.polarity > 0:
                sentiment_results["positive"] += 1
            elif analysis.sentiment.polarity == 0:
                sentiment_results["neutral"] += 1
            else:
                sentiment_results["negative"] += 1

        return render_template('stocks/sentiment.html', stock_symbol=stock_symbol, sentiment_results=sentiment_results, headlines=headlines)

    return render_template('stocks/sentiment.html')


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


@stocks_blueprint.route("/chartjs_demo1")
def chartjs_demo1():
    return render_template('stocks/chartjs_demo1.html')

@stocks_blueprint.route("/chartjs_demo2")
def chartjs_demo2():
    title = 'Monthly Data'
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August']
    values = [10.3, 9.2, 8.7, 7.1, 6.0, 4.4, 7.6, 8.9]
    return render_template('stocks/chartjs_demo2.html', values=values, labels=labels, title=title)

@stocks_blueprint.route("/chartjs_demo3")
def chartjs_demo3():
    title = 'Daily Prices'
    labels = [datetime(2020, 2, 10),   # Monday 2/10/2020
              datetime(2020, 2, 11),   # Tuesday 2/11/2020
              datetime(2020, 2, 12),   # Wednesday 2/12/2020
              datetime(2020, 2, 13),   # Thursday 2/13/2020
              datetime(2020, 2, 14),   # Friday 2/14/2020
              datetime(2020, 2, 17),   # Monday 2/17/2020
              datetime(2020, 2, 18),   # Tuesday 2/18/2020
              datetime(2020, 2, 19)]   # Wednesday 2/19/2020
    values = [10.3, 9.2, 8.7, 7.1, 6.0, 4.4, 7.6, 8.9]
    return render_template('stocks/chartjs_demo3.html', values=values, labels=labels, title=title)





@stocks_blueprint.route('/stocks/<id>')
@login_required
def stock_details(id):
    query = database.select(Stock).where(Stock.id == id)
    stock = database.session.execute(query).scalar_one_or_none()

    if stock is None:
        abort(404)

    if stock.user_id != current_user.id:
        abort(403)

    title, labels, values = stock.get_weekly_stock_data()
    return render_template('stocks/stock_details.html', stock=stock, title=title, labels=labels, values=values)