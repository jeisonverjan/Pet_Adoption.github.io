from flask import Blueprint
from . import db
from .models import Country, State

views = Blueprint('views', __name__)

@views.route('/')
def home():
    #colombia = Country(code= 53, name='Colombia')
    #colombia = Country.query.filter(Country.code==53).first()
    colombia = State(code= 20, name='Kansas', country_code = 1)
    db.session.add(colombia)
    db.session.commit()
    print('El usuario se ha agregado a la base de datos')
    return "<h1> Test </h1>"