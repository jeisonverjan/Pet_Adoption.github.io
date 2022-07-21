from flask import Blueprint, flash, jsonify, render_template, request
from . import create_app, db
from flask_login import login_required, current_user
from .models import *
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, TextAreaField, SubmitField
from flask_wtf.file import FileField
import os
from werkzeug.utils import secure_filename
import uuid as uuid
from flask import current_app


views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Post_form(FlaskForm):
    pet_type = SelectField('Country', choices=[])
    breed = SelectField('State', choices=[], validators=[validators.InputRequired()])
    code = StringField("Code", validators=[validators.InputRequired(), validators.Length(max=50)], render_kw={"placeholder": "Pet Code"})
    name= StringField("Name", validators=[validators.InputRequired(), validators.Length(min=3,max=50)], render_kw={"placeholder": "Name"})
    sex = SelectField('Sex', choices=['Male', 'Female'])
    age = SelectField('Sex', choices=['Less than 1 year', 'Between 1 and 3 years', 'Between 3 and 5 years', 'Older than 5 years'])
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
            pet_pic_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],  pic_name))
            new_media = Media(path=pic_name, pet_code=1)
            db.session.add(new_media)
            db.session.commit()
            flash('The picture has been upload', category='success')       
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