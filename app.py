from pydantic import BaseModel, field_validator, ValidationError
from flask import session, Flask, render_template, request, redirect, url_for
from flask.logging import default_handler
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


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

app.secret_key = "temp"





from project.stocks import stocks_blueprint
from project.users import users_blueprint

app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')

