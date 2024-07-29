"""Module containing Database Initialization script"""
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

load_dotenv()

DBTYPE = os.getenv('DBTYPE')
DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')
HOSTNAME = os.getenv('HOSTNAME')
DBNAME = os.getenv('DBNAME')
DBPORT = os.getenv('DBPORT')

DB_URL = f"{DBTYPE}://{DBUSER}:{DBPASS}@{HOSTNAME}:{DBPORT}/{DBNAME}"

# Creating the engine
engine = create_engine(DB_URL)

# Creating the Base class
Base = declarative_base()

# Creating the session class
Session = sessionmaker(bind=engine)


def get_session():
    """Function to return the Session class"""
    return Session()


def initialize_database():

    # Create all tables in the engine
    Base.metadata.create_all(engine)
