from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "project"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/aboutus')
    app.register_blueprint(auth, url_prefix='/auth')


    return app

