"""Module to define blueprints for Flask app"""
from API.user_endpoint import users_bp
from flask import blueprints


def define(app):
    """Function to define blueprints for Flask app"""

    # Users endpoint
    app.register_blueprint(users_bp, url_prefix='/users')

    return app
