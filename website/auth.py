from flask import Blueprint, render_template
from . import db
from .models import *

auth = Blueprint('aut', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<h2> Logout Page <h2>"


