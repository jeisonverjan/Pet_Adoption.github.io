from flask import Blueprint, render_template
from flask_login import current_user
from .models import *


indexs = Blueprint('index', __name__)



@indexs.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html", user=current_user, posts=posts)