"""File for initializing services."""
from services.Database.database import initialize_database

from .countries_initializer import initialize_countries


def initialize_services():
    """Initialize services."""

    # Initialize database with models
    initialize_database()

    # Add all countries to database
    initialize_countries()
