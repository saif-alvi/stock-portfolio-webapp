from . import users_blueprint
from flask import render_template, flash

@users_blueprint.route('/about')
def about():
    # return render_template('about.html', company_name="TestDriven.io")
    flash('Thanks for being a user!', 'info')
    return render_template('users/about.html', company_name='Saif Alvi')
