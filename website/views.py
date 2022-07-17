from flask import Blueprint, render_template
from . import db
from .models import *

views = Blueprint('views', __name__)

@views.route('/')
def home():
    #colombia = Country(code= 53, name='Colombia')
    #colombia = State(code= 20, name='Kansas', country_code = 1)
    #db.session.add(colombia)
    #db.session.commit()
    #country = Country.query.get(3)
    
    return render_template("home.html")