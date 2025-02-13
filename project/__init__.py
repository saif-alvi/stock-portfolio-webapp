from flask import Flask, render_template
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os
from flask_migrate import Migrate


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_app_callbacks(app)
    register_error_pages(app)
    return app



#DataBase naming Convention:

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# --------Config -----
metadata = MetaData(naming_convention=convention)
database = SQLAlchemy(metadata=metadata)
db_migration = Migrate()
# --------------------


# Helper Functions
def initialize_extensions(app):
    database.init_app(app)
    db_migration.init_app(app,database)







def register_blueprints(app):
    # Import the blueprints
    from project.stocks import stocks_blueprint
    from project.users import users_blueprint

    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)

    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')

def configure_logging(app):
    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    # Logging Configuration
    file_handler = RotatingFileHandler('instance/flask-stock-portfolio.log', maxBytes=16384, backupCount=20)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Starting the Flask Stock Portfolio App...')


def register_app_callbacks(app):
    
    @app.before_request
    def app_before_request():
        app.logger.info('Calling before_request() for the Flask application...')
    
    @app.after_request
    def app_after_request(response):
        app.logger.info('Calling after_request() for the Flask application...')
        return response
    
    @app.teardown_request
    def app_teardown_request(error=None):
        app.logger.info('Calling teardown_request() for the Flask application...')
    
    @app.teardown_appcontext
    def app_teardown_appcontext(error=None):
        app.logger.info('Calling teardown_appcontext() for the Flask application...')

def register_error_pages(app):
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(405)
    def page_not_found(e):
        return render_template('405.html'), 405
