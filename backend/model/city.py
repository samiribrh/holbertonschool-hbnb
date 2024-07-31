"""Module containing City class"""
from services.Validators.validators import Validator
from services.Database.database import Base, get_session
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import validates
from datetime import datetime
from uuid import uuid4


class City(Base):
    """The City Class"""
    __tablename__ = 'cities'

    id = Column(String(36), primary_key=True, default=lambda: uuid4())
    name = Column(String(255), nullable=False)
    country = Column(String(2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        """Function to validate name"""

        # Check if name is empty
        if not value:
            raise ValueError("Name cannot be empty")

        # Make name words start with uppercase
        validated_name = ' '.join(word.capitalize() for word in value.split())
        return validated_name

    @validates('country')
    def validate_country(self, key, value):
        validated_country = value.upper()
        if not Validator.validate_country(validated_country):
            raise ValueError('Invalid country value')
        if Validator.validate_city_in_country(self.name, value):
            raise ValueError("City already exists")
        return validated_country

    @staticmethod
    def delete(deletionid: str):
        from model.place import Place

        session = get_session()
        try:
            citytodelete = session.query(City).filter(City.id == deletionid).one()
            if not citytodelete:
                raise ValueError("City does not exist")
            placesincity = session.query(Place).filter(Place.city == deletionid).all()
            for place in placesincity:
                Place.delete(place.id)
                session.commit()
            session.delete(citytodelete)
            session.commit()
            return citytodelete
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
