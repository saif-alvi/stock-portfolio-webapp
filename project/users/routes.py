from . import users_blueprint
from flask import render_template, flash, abort

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