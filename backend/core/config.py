import os
from dotenv import load_dotenv

load_dotenv("../")


class Config:
    DBTYPE = os.getenv('DBTYPE', 'postgresql+psycopg2')
    DBUSER = os.getenv('DBUSER', 'root')
    DBPASS = os.getenv('DBPASSWORD', 'password')
    HOSTNAME = os.getenv('HOSTNAME', 'localhost')
    DBNAME = os.getenv('DBNAME', 'database')
    DBPORT = os.getenv('DBPORT', 5432)

    SQLALCHEMY_DATABASE_URL = f"{DBTYPE}://{DBUSER}:{DBPASS}@{HOSTNAME}:{DBPORT}/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    COUNTRYFILE = os.getenv('COUNTRYFILE', 'backend/data/countries.json')
