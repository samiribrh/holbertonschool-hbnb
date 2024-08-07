"""Module containing Country class"""
from datetime import datetime

from sqlalchemy import Column, VARCHAR, DateTime

from services.Database.database import Base


class Country(Base):
    """The Country Class"""
    __tablename__ = 'countries'

    id = Column(VARCHAR(2), primary_key=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
