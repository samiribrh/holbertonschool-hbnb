import os
from dotenv import load_dotenv

load_dotenv("../")


class Config:
    DBTYPE = os.getenv('DBTYPE', 'postgresql+psycopg2')
    DBUSER = os.getenv('POSTGRES_USER', 'root')
    DBPASS = os.getenv('POSTGRES_PASSWORD', 'password')
    HOSTNAME = os.getenv('HOSTNAME', 'localhost')
    DBNAME = os.getenv('POSTGRES_DB', 'database')
    DBPORT = os.getenv('DBPORT', 5432)

    SQLALCHEMY_DATABASE_URL = f"{DBTYPE}://{DBUSER}:{DBPASS}@{HOSTNAME}:{DBPORT}/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    STATIC_FOLDER = os.getenv('STATIC_FOLDER', 'app/static')
    COUNTRYFILE = os.getenv('COUNTRYFILE', 'app/data/countries.json')
