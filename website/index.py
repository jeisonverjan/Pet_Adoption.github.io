from flask import Blueprint, render_template
from flask_login import current_user

indexs = Blueprint('index', __name__)

@indexs.route('/')
def index():
        
    return render_template("index.html", user=current_user)