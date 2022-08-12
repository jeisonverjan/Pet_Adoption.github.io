from click import style
from flask import Blueprint, render_template
from flask_login import current_user
from .models import *
from . import db
import random


indexs = Blueprint('index', __name__)



@indexs.route('/')
def index():
    posts = db.engine.execute('SELECT post.id, media.path, pet.name, post.description FROM media, pet, post WHERE media.pet_id = post.pet_id AND post.pet_id = pet.id')
    random_style = str(random.randint(1, 6))
    return render_template("index.html", user=current_user, posts=posts, random_style=random_style)