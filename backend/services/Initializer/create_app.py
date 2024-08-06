"""Module to create Flask app"""
from services.Initializer.define_blueprints import define_blueprints
from core.config import Config
from flask_jwt_extended import JWTManager
from flask import Flask


class FlaskApp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FlaskApp, cls).__new__(cls)
            cls._instance.options = None
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the Flask app."""
        self.app = Flask(__name__, static_folder=Config.STATIC_FOLDER, static_url_path='/' + Config.STATIC_FOLDER)
        self.app.config.from_object(Config)
        self.jwt = JWTManager(self.app)
        self.app = define_blueprints(self.app)

    def get_app(self):
        """Return the Flask app instance."""
        return self.app
