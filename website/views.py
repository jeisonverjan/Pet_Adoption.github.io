from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import *

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    #colombia = Country(code= 53, name='Colombia')
    #colombia = State(code= 20, name='Kansas', country_code = 1)
    #db.session.add(colombia)
    #db.session.commit()
    country = City.query.all()
    
    return render_template("home.html", country=country, user=current_user)