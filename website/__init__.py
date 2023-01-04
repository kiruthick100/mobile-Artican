from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from flask_mail import Mail,Message

db = SQLAlchemy()
mail=Mail()

DB_NAME = "workers.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] ='kiruthick'
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] ='smtp.gmail.com'
    app.config['MAIL_PORT'] =465
    app.config['MAIL_USERNAME']='kiruthickkumark.20cse@kongu.edu'
    app.config['MAIL_PASSWORD']="k16072003k"
    app.config['MAIL_USE_TLS'] =False
    app.config['MAIL_USE_SSL']=True
    mail.init_app(app)

    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    create_database(app)
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    from .models import User,Data
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app): 
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        
