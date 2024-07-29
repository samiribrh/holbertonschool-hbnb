import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DBTYPE = os.getenv('DBTYPE', 'sqlite')
    DBUSER = os.getenv('DBUSER', 'user')
    DBPASS = os.getenv('DBPASS', 'password')
    HOSTNAME = os.getenv('HOSTNAME', 'localhost')
    DBNAME = os.getenv('DBNAME', 'database')
    DBPORT = os.getenv('DBPORT', 3306)

    SQLALCHEMY_DATABASE_URI = f"{DBTYPE}://{DBUSER}:{DBPASS}@{HOSTNAME}:{DBPORT}/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    COUNTRYFILE = os.getenv('COUNTRYFILE', 'backend/Data/countries.json')
