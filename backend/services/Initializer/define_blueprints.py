"""Module to define blueprints for Flask app"""
from api.amenities_endpoint import amenities_bp
from api.auth import auth_bp
from api.cities_endpoint import cities_bp
from api.countries_endpoint import countries_bp
from api.places_endpoint import places_bp
from api.reviews_endpoint import reviews_bp
from api.static_endpoint import static_bp
from api.status_endpoint import status_bp

from services.swagger import swagger_blueprint, SWAGGER_URL


def define_blueprints(app):
    """Function to define blueprints for Flask app"""

    # Users endpoint
    app.register_blueprint(users_bp, url_prefix='/users')

    # Auth endpoint
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Countries and Cities endpoints
    app.register_blueprint(countries_bp, url_prefix='/countries')
    app.register_blueprint(cities_bp, url_prefix='/cities')

    # Amenities endpoint
    app.register_blueprint(amenities_bp, url_prefix='/amenities')

    # Places endpoint
    app.register_blueprint(places_bp, url_prefix='/places')

    # Reviews endpoint
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    # Static endpoint
    app.register_blueprint(static_bp, url_prefix='/static')

    # Swagger endpoint
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    # Status endpoint
    app.register_blueprint(status_bp, url_prefix='/status')

    return app
