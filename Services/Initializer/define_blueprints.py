"""Module to define blueprints for Flask app"""
from API.user_endpoint import users_bp
from API.countries_endpoint import countries_bp
from API.cities_endpoint import cities_bp


def define_blueprints(app):
    """Function to define blueprints for Flask app"""

    # Users endpoint
    app.register_blueprint(users_bp, url_prefix='/users')

    # Countries and Cities endpoints
    app.register_blueprint(countries_bp, url_prefix='/countries')
    app.register_blueprint(cities_bp, url_prefix='/cities')

    return app
