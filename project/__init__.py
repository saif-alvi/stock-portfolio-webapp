from flask import Flask, render_template
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from sqlalchemy.exc import NoResultFound
from flask_mail import Mail

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
csrf_protection = CSRFProtect()
login = LoginManager()            
login.login_view = "users.login"
mail = Mail()
# --------------------


# Helper Functions
def initialize_extensions(app):
    database.init_app(app)
    db_migration.init_app(app,database)
    csrf_protection.init_app(app)
    login.init_app(app)
    mail.init_app(app)


    # Flask-Login configuration
    from project.models import User

    @login.user_loader
    def load_user(user_id):
        try:
            print(f"Loading user with ID: {user_id}")  # Debugging statement
            user = database.session.query(User).filter(User.id == int(user_id)).one()
            print(f"Loaded user: {user}")  # Debugging statement
            print(f"User ID: {user.id}")  # Debugging statement
            return user
        except NoResultFound:
            print(f"No user found with ID: {user_id}")  # Debugging statement
            return None





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
    @app.errorhandler(403)
    def page_forbidden(e):
        return render_template('403.html'), 403