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

    # Redis configuration
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

    # Email configuration
    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_MAIL = os.getenv('SMTP_MAIL')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    VERIFICATION_EXPIRATION = 60 * 3

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')

    # Static file path
    STATIC_FOLDER = '/app/static'

    # Country file path
    COUNTRYFILE = '/app/data/countries.json'
