from email.policy import default
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from . import db
from .models import *
from wtforms import SelectField, StringField, validators, EmailField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user

sign_up = Blueprint('signup', __name__)


class Sign_up_form(FlaskForm):
    name = StringField("Name", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Name"})
    last_name = StringField("Name", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Last Name"})
    email = EmailField("Email", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Email"})
    phone = StringField("Phone", validators=[validators.InputRequired()], render_kw={"placeholder": "Phone Number"})
    password1 = PasswordField("Password1", validators=[validators.InputRequired(), validators.Length(min=3,max=15)], render_kw={"placeholder": "Password"})
    password2 = PasswordField("Password1", validators=[validators.InputRequired(), validators.Length(min=3,max=15)], render_kw={"placeholder": "Re-enter Password"})
    country = SelectField('country', choices=[])
    state = SelectField('state', choices=[])
    city = SelectField('city', choices=[], validators=[validators.InputRequired()])
    address = StringField("Address", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Address"})
    send = SubmitField("Send Record")



@sign_up.route('/sign_up', methods=['GET', 'POST'])
def signup(): 
    form = Sign_up_form()
    form.country.data = 'Select Country'
    user = User.query.filter_by(mail=form.email.data).first()
    form.country.choices = [(country.id, country.name) for country in Country.query.all()]

    if request.method == 'POST':
        if user != None:
            flash('Email alredy exists', category="error")
        elif form.password1.data != form.password2.data:
            flash('Password don\'t match', category='error')
        else:
            new_user = User(name= form.name.data, last_name=form.last_name.data, mail= form.email.data, address = form.address.data, phone=form.phone.data, password=generate_password_hash(form.password1.data, method='sha256'), user_profile_id = 1, city_code= form.city.data)
            db.session.add(new_user)
            db.session.commit()
            flash('The user has been created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", form=form, user=current_user)


@sign_up.route('/state/<get_state>')
def statebycountry(get_state):
    state = State.query.filter_by(country_id=get_state).all()
    stateArray = []
    for city in state:
        stateObj = {}
        stateObj['id'] = city.id
        stateObj['name'] = city.name
        stateArray.append(stateObj)
    return jsonify({'statecountry' : stateArray})

@sign_up.route('/city/<get_city>')
def city(get_city):
    state_data = City.query.filter_by(state_id=get_city).all()
    cityArray = []
    for city in state_data:
        cityObj = {}
        cityObj['id'] = city.id
        cityObj['name'] = city.name
        cityArray.append(cityObj)
    return jsonify({'citylist' : cityArray}) 