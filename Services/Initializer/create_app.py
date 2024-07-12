"""Module to create Flask app"""
from Services.Initializer.define_blueprints import define_blueprints
from flask_jwt_extended import JWTManager
from flask import Flask


def create_app():
    """Function to create flask app with configurations"""
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'akeycouldbemaximumthismuchsafe'
    jwt = JWTManager(app)

    app = define_blueprints(app)

    return app
