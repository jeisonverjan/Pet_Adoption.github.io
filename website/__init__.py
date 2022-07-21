from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "Pet_Adoption.db"


def create_app():
    app = Flask(__name__)
    UPLOAD_FOLDER = 'website/static/images/pet_media/'
    app.config['SECRET_KEY'] = 'Pet_Adoption 0.1'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    
    db.init_app(app)
    
    

    from .views import views
    from .auth import auth
    from .sign_up import sign_up
    from .index import indexs
    from .models import Country, State, City, User_profile, Pet_type, Breed, Pet, Post, User
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(sign_up, url_prefix='/')
    app.register_blueprint(indexs, url_prefix='/')
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'index.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')