import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from extensions import db, mail, bcrypt, login_manager

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(config_class=Config):
    """
    Creates a flask app with a given configuration
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    register_blueprints(app)
    register_extensions(app)

    return app


def register_extensions(app):
    """
    Register extensions used with this app
    """
    with app.app_context():
        db.init_app(app)
        Migrate(app, db)
        mail.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = "users_blueprint.login"
        login_manager.login_message_category = "info"


def register_blueprints(app):
    """
    Register blueprints
    """
    from flask_blog.users.views import users_blueprint
    from flask_blog.posts.views import posts_blueprint
    from flask_blog.public.views import public_blueprint
    from flask_blog.errors.views import errors_blueprint

    with app.app_context():
        app.register_blueprint(users_blueprint)
        app.register_blueprint(posts_blueprint)
        app.register_blueprint(public_blueprint)
        app.register_blueprint(errors_blueprint)
