from flask import Blueprint, flash, jsonify, render_template, request, url_for
from . import db
from flask_login import login_required, current_user
from .models import *
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, TextAreaField, SubmitField
from flask_wtf.file import FileField
import os
from werkzeug.utils import secure_filename
import uuid as uuid
from flask import current_app
import json


views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Post_form(FlaskForm):
    pet_type = SelectField('Select the type of pet:', choices=[])
    breed = SelectField('Select the breed of the pet:', choices=[], validators=[validators.InputRequired()])
    name= StringField("Enter the Name of the pet:", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Name"})
    sex = SelectField('Select the sex of the pet:', choices=['Male', 'Female'])
    age = SelectField('Select the age of the pet:', choices=[(0, "Select pet's age"), (1, 'Less than 1 year'), (2, 'Between 1 and 3 years'), (3, 'Between 3 and 5 years'), (4, 'Older than 5 years')])
    pet_pic = FileField('Upload a pet\'s picture', validators=[validators.InputRequired()])
    description = TextAreaField("Code", validators=[validators.Length(max=100)], render_kw={"placeholder": "Writh a pet\'s description"})
    send = SubmitField("Send Post")



@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = Post_form()
    form.pet_type.choices = [(pet_type.id, pet_type.name) for pet_type in Pet_type.query.all()]
    pet_pic_file = form.pet_pic.data
    
    if request.method == 'POST':
        if  pet_pic_file and allowed_file( pet_pic_file.filename):
            pic_filename = secure_filename( pet_pic_file.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Adding pet to the data base
            new_pet = Pet(name=form.name.data, age=form.age.data, sex=form.sex.data, pet_type_id=form.pet_type.data, breed_id=form.breed.data)
            db.session.add(new_pet)
            db.session.commit()
            # Adding a new post to the data base
            new_post = Post(description=form.description.data, user_id=current_user.id, pet_id=new_pet.id)
            # Adding photo to the data base.
            
            new_media = Media(path=pic_name, pet_id=new_pet.id)
            db.session.add(new_media)
            db.session.add(new_post)
            db.session.commit()
            #saving the picture in the folder
            pet_pic_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],  pic_name))
            flash('The Post has been upload', category='success')       
        else:
            flash('Enter a valid file (png, jpg, jpeg, gif)', category='error')   
        
    return render_template("home.html", user=current_user, form=form)

@views.route('/breed/<get_breed>')
def breedbytype(get_breed):
    breed = Breed.query.filter_by(pet_type_id = get_breed).all()
    breedArray = []
    for element in breed:
        breedObj = {}
        breedObj['id'] = element.id
        breedObj['name'] = element.name
        breedArray.append(breedObj)

    return jsonify({'breedbytype' : breedArray})

@views.route('/home/posts', methods=['GET', 'POST'])
@login_required
def user_posts():
    form = Post_form()
    posts = db.engine.execute("SELECT post.id, media.path, pet.name, post.description FROM media, pet, post WHERE media.pet_id = post.pet_id AND post.pet_id = pet.id AND post.status = True AND  post.user_id =" + str(current_user.id))
    db.session.commit()
    return render_template("user_posts.html", user=current_user, form=form, posts=posts)


@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    petId = post.pet_id
    pet = Pet.query.get(petId)
    media = Media.query.filter_by(pet_id = int(petId)).first()
    if post:        
        if current_user.id == int(post.user_id):
            db.session.delete(post)
            db.session.delete(pet)
            db.session.delete(media)
            db.session.commit()
            flash(" Post Deleted ", category='Success')        
   
        
    return jsonify({})
