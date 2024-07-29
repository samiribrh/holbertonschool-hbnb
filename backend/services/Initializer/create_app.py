"""Module to create Flask app"""
from services.Initializer.define_blueprints import define_blueprints
from core.config import Config
from flask_jwt_extended import JWTManager
from flask import Flask


def create_app():
    """Function to create flask app with configurations"""
    app = Flask(__name__, static_folder='../../static', static_url_path='/../../static')

    app.config.from_object(Config)
    jwt = JWTManager(app)

    app = define_blueprints(app)

    return app
