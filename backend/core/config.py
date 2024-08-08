"""Configuration module for settings and environment variables."""
import os

from dotenv import load_dotenv


load_dotenv("../")


class Config:
    # Database configuration
    DBTYPE = os.getenv('DBTYPE', 'postgresql+psycopg2')
    DBUSER = os.getenv('POSTGRES_USER', 'root')
    DBPASS = os.getenv('POSTGRES_PASSWORD', 'password')
    HOSTNAME = os.getenv('HOSTNAME', 'localhost')
    DBNAME = os.getenv('POSTGRES_DB', 'database')
    DBPORT = int(os.getenv('DBPORT', 5432))

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URL = f"{DBTYPE}://{DBUSER}:{DBPASS}@{HOSTNAME}:{DBPORT}/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')

    # Static file path
    STATIC_FOLDER = '/app/static'

    # Country file path
    COUNTRYFILE = '/app/data/countries.json'
