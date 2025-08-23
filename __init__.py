from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = "database.db"


def create_database(app):
    if not path.exists('website/' + DB_Name):
        with app.app_context():
            db.create_all()
            print('Created Database!')
    else:
        print('Database already exists.')



def create_app():
    app  = Flask(__name__)
    app.config['SECRET_KEY'] = 'MINI IT'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Note, User
    with app.app_context():
        db.create_all()  

    create_database(app)

    return app




