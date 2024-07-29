"""Module to define blueprints for Flask app"""
from API.users_endpoint import users_bp
from API.countries_endpoint import countries_bp
from API.cities_endpoint import cities_bp
from API.amenities_endpoint import amenities_bp
from API.places_endpoint import places_bp
from API.reviews_endpoint import reviews_bp


def define_blueprints(app):
    """Function to define blueprints for Flask app"""

    # Users endpoint
    app.register_blueprint(users_bp, url_prefix='/users')

    # Countries and Cities endpoints
    app.register_blueprint(countries_bp, url_prefix='/countries')
    app.register_blueprint(cities_bp, url_prefix='/cities')

    # Amenities endpoint
    app.register_blueprint(amenities_bp, url_prefix='/amenities')

    # Places endpoint
    app.register_blueprint(places_bp, url_prefix='/places')

    #
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    return app
