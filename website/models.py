from . import db

class State(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    country_code = db.Column(db.Integer, db.ForeignKey('country.code'))

class Country(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    states = db.relationship(State)