"""Module to create Flask app"""
import os

from Services.Initializer.define_blueprints import define_blueprints
from flask_jwt_extended import JWTManager
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """Function to create flask app with configurations"""
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    app = define_blueprints(app)

    return app
