from flask import Blueprint
from flask import render_template

views = Blueprint('views',__name__)

@views.route('/aboutus')
def home():
    return render_template('aboutus.html', text='Home Page')
