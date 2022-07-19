from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# User Data

class City(db.Model):
    id =   db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

class State(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    states = db.relationship(City)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    states = db.relationship(State)

class User_profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

# Pet Data

class Pet_type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

class Breed(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(350), nullable = False)
    pet_type_id = db.Column(db.Integer, db.ForeignKey('pet_type.id'))

class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    path = db.Column(db.String(150), nullable = False)
    pet_code = db.Column(db.Integer, db.ForeignKey('pet.code'))

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    birth = db.Column(db.Date)
    sex = db.Column(db.String(100), nullable = False)
    status = db.Column(db.Boolean, default = True)
    pet_type_id = db.Column(db.Integer, db.ForeignKey('pet_type.id'))
    breed_id = db.Column(db.Integer, db.ForeignKey('breed.id'))
    medias = db.relationship(Media)

# Post Data

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(100), nullable = False)
    status = db.Column(db.Boolean, default = True)
    user_mail = db.Column(db.String, db.ForeignKey('user.mail'))
    pet_code = db.Column(db.Integer, db.ForeignKey('pet.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    mail = db.Column(db.String(100), unique = True, nullable = False)
    address = db.Column(db.String(150), nullable = False)
    phone = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(45), nullable = False)
    status = db.Column(db.Boolean, default = True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    city_code = db.Column(db.Integer, db.ForeignKey('city.id'))
    posts = db.relationship(Post)
