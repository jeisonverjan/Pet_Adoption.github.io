from flask import Blueprint, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, validators, EmailField, SubmitField, TextAreaField
from flask_login import current_user
import json
from .models import *

adoption = Blueprint('adoption', __name__)

class Adoption_request(FlaskForm):
    name = StringField("Name", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Name"})
    last_name = StringField("Name", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Last Name"})
    email = EmailField("Email", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Email"})
    phone = StringField("Phone", validators=[validators.InputRequired()], render_kw={"placeholder": "Phone Number"})
    description = TextAreaField("Code", validators=[validators.Length(max=100)], render_kw={"placeholder": "Additional information"})
    send = SubmitField("Send Request")

@adoption.route('/adoption_request', methods=['GET', 'POST'])
def adoption_request():    
    form = Adoption_request() 

    return render_template("pet_info.html", form=form, user=current_user)

@adoption.route('/pet_info', methods=['POST'])
def petInfo():

    post = json.loads(request.data)
    postId = post['postId']
    posts = posts = db.engine.execute("SELECT pet_type.name type, breed.name breed, pet.name pet_name, pet.age pet_age, pet.sex pet_sex, city.name pet_city FROM pet_type, breed, pet, post, user, city WHERE pet_type.id = pet.pet_type_id and breed.id = pet.breed_id and pet.id = post.pet_id and post.user_id = user.id and user.city_code = city.id and post.id =" + str(postId))
    db.session.commit()
    postArray = []
    for post in posts:
        postObj = {}
        postObj['pet_type_name'] = post.type
        postObj['breed_name'] = post.breed
        postObj['pet_name'] = post.pet_name
        postObj['pet_age'] = post.pet_age
        if postObj['pet_age'] == "1":
           postObj['pet_age'] = "Less than one year"
        elif postObj['pet_age'] == "2":
            postObj['pet_age'] = "Between 1 and 3 years"
        elif postObj['pet_age'] == "3":
            postObj['pet_age'] = "Between 3 and 5 years"
        elif postObj['pet_age'] == "4":
            postObj['pet_age'] = "Older than 5 years"
        postObj['pet_sex'] = post.pet_sex
        postObj['city_name'] = post.pet_city
        postArray.append(postObj)
        

    return jsonify({'postObject' : postArray})



