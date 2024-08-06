"""Module containing Database Initialization script"""
from core.config import Config
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import psycopg2

load_dotenv()

DB_URL = Config.SQLALCHEMY_DATABASE_URL

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
    """Function to initialize the database"""

    # Create all tables in the engine
    Base.metadata.create_all(engine)
