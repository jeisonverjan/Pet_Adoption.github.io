import imp
from flask import Blueprint, render_template, request, jsonify, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, validators, EmailField, SubmitField, TextAreaField
from flask_login import current_user
import json
from .models import *
from email.message import EmailMessage
import ssl
import smtplib


adoption = Blueprint('adoption', __name__)

class Adoption_request(FlaskForm):
    post_id = StringField("Post ID")
    pet_type = StringField("Pet Type")
    pet_name = StringField("Pet Name")
    pet_age = StringField("Pet Age")
    pet_breed = StringField("Pet Breed")
    pet_sex = StringField("Pet Sex")
    pet_city = StringField("Pet City")
    name = StringField("Name", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Name"})
    last_name = StringField("Name", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Last Name"})
    email = EmailField("Email", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Email"})
    phone = StringField("Phone", validators=[validators.InputRequired()], render_kw={"placeholder": "Phone Number"})
    description = TextAreaField("Code", validators=[validators.Length(max=100)], render_kw={"placeholder": "Additional information"})
    send = SubmitField("Send Request")


@adoption.route('/adoption_request', methods=['GET', 'POST'])
def adoption_request():    
    form = Adoption_request()
    if request.method == 'POST':
        post_id = form.post_id.data
        pet_info = {'type': form.pet_type.data, 'name': form.pet_name.data, 'age': form.pet_age.data, 'breed': form.pet_breed.data, 'sex': form.pet_sex.data}
        requester_info = {'name': form.name.data, 'last_name': form.last_name.data, 'email': form.email.data, 'phone': form.phone.data, 'description': form.description.data}
        user_email = db.engine.execute("SELECT user.mail mail from user, post where user.id = post.user_id and post.id = " + str(post_id))
        for mail in user_email:
            user_email = mail.mail
        sendEmail(pet_info, requester_info, user_email)

    return render_template("pet_info.html", form=form, user=current_user)


@adoption.route('/pet_info', methods=['POST'])
def petInfo():
    
    post = json.loads(request.data)
    postId = post['postId']
    posts = db.engine.execute("SELECT pet_type.name type, breed.name breed, pet.name pet_name, pet.age pet_age, pet.sex pet_sex, city.name pet_city, user.mail user_mail FROM pet_type, breed, pet, post, user, city WHERE pet_type.id = pet.pet_type_id and breed.id = pet.breed_id and pet.id = post.pet_id and post.user_id = user.id and user.city_code = city.id and user.id = post.user_id and post.id =" + str(postId))
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
        postObj['user_mail'] = post.user_mail
        postArray.append(postObj)    

    return jsonify({'postObject' : postArray})


def sendEmail(pet_info, requester_info, user_email):
    email_sender = 'dejemesano995@gmail.com'
    email_password = 'xvabpzkfucjaphqw'
    email_receiver = user_email

    subject = 'Pet Adoption Request'
    body = f"Dear {pet_info['name']} owner, \n\n You have received an adoption request from {requester_info['name']} who is interested in adopting {pet_info['name']} \n Below you can find the requester information so you can contact him/her: \n\n Requester information: \n\n Name: {requester_info['name']} {requester_info['last_name']} \n Email: {requester_info['email']} \n Phone number: {requester_info['phone']} \n Additional Information: {requester_info['description']} \n\n Pet information: \n\n Name: {pet_info['name']} \n Type: {pet_info['type']} \n Breed: {pet_info['breed']} \n Age: {pet_info['age']} \n Sex: {pet_info['sex']} \n\n Regards, \n PetAdoption team"
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    flash(f"An email has been sent to the owner of {pet_info['name']}, who will contact you with more information.", category='success')

