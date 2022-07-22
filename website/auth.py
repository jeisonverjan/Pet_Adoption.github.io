from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import *
from flask_wtf import FlaskForm
from wtforms import validators, EmailField, PasswordField, SubmitField
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('aut', __name__)

class Login_form(FlaskForm):
    email = EmailField("Email", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[validators.InputRequired(), validators.Length(min=3,max=15)], render_kw={"placeholder": "Password"})
    send = SubmitField("Login")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_form()
    
    if request.method == 'POST':
        user = User.query.filter_by(mail=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data) and user.status == True:
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect, try again', category='error')
        else:
            flash('The user does not exist', category='error')
    return render_template('login.html', form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index'))


