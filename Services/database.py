"""Module containing Database Initialization script"""
from env.env import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Creating the engine
engine = create_engine(DB_URL, echo=True)

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
