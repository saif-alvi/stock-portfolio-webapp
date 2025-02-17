from . import users_blueprint
from flask import render_template, flash, abort, request, current_app, redirect, url_for
from .forms import RegistrationForm
from project.models import User
from project import database
from sqlalchemy.exc import IntegrityError
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, login_required, logout_user

@users_blueprint.route('/about')
def about():
    # return render_template('about.html', company_name="TestDriven.io")
    flash('Thanks for being a user!', 'info')
    return render_template('users/about.html', company_name='Saif Alvi')

@users_blueprint.errorhandler(403)
def page_forbidden(e):
    return render_template('users/403.html'), 403


@users_blueprint.route('/admin')
def admin():
    abort(403)

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                database.session.add(new_user)
                database.session.commit()
                flash(f'Thanks for registering, {new_user.email}!')
                current_app.logger.info(f'Registered new user: {form.email.data}!')
                return redirect(url_for('stocks.index'))
            except IntegrityError:
                database.session.rollback()
                flash(f'ERROR! Email ({form.email.data}) already exists.', 'error')
        else:
            flash(f"Error in form data!")

    return render_template('users/register.html', form=form)



@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('stocks.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            query = database.select(User).where(User.email == form.email.data)
            user = database.session.execute(query).scalar_one()

            if user and user.is_password_correct(form.password.data):
                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f'Thanks for logging in, {current_user.email}!')
                current_app.logger.info(f'Logged in user: {current_user.email}')
                return redirect(url_for('stocks.index'))

        flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    current_app.logger.info(f'Logged out user: {current_user.email}')
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('stocks.index'))

@users_blueprint.route('/profile')
@login_required
def user_profile():
    return render_template('users/profile.html')