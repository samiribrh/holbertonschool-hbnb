"""Module containing Place class"""
from services.Validators.validators import Validator
from services.Database.database import Base, get_session
from sqlalchemy import Column, String, Text, Float, Integer, DateTime
from sqlalchemy.orm import validates
from datetime import datetime
from uuid import uuid4


class Place(Base):
    """The Place Class"""
    __tablename__ = 'places'

    id = Column(String(36), primary_key=True, default=lambda: uuid4())
    name = Column(String(255), nullable=False)
    description = Column(Text)
    address = Column(String(255), nullable=False)
    city = Column(String(36), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host = Column(String(36), nullable=False)
    num_of_rooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    max_guests = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow(), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Name cannot be empty')
        return value

    @validates('address')
    def validate_address(self, key, value):
        validated_address = ' '.join(word.capitalize() for word in value.split())
        if not Validator.validate_address(value):
            raise ValueError("Place with this address already exists")
        return validated_address

    @validates('city')
    def validate_city(self, key, value):
        validated_city = value.lower()
        if not Validator.validate_city(validated_city):
            raise ValueError("City not valid")
        return validated_city

    @validates('latitude')
    def validate_latitude(self, key, value):
        if value < -90 or value > 90:
            raise ValueError("Latitude not valid")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if value < -180 or value > 180:
            raise ValueError("Longitude not valid")
        return value

    @validates('host')
    def validate_host(self, key, value):
        validated_host = value.lower()
        if not Validator.validate_user_by_id(validated_host):
            raise ValueError("Host not valid")
        return validated_host

    @validates('num_of_rooms', 'bathrooms', 'max_guests')
    def validate_posint(self, key, value):
        if value <= 0:
            raise ValueError("num_of_rooms, bathrooms, max_guests must be positive integers")
        return value

    @staticmethod
    def delete(deletionid: str):
        """Function to delete a Place object"""
        from model.place_amenity import PlaceAmenity

        session = get_session()
        try:
            placetodelete = session.query(Place).filter(Place.id == deletionid).one()
            if not placetodelete:
                raise ValueError("Place not exists")
            amenity_place = session.query(PlaceAmenity).filter(PlaceAmenity.place_id == deletionid).all()
            for amenityobj in amenity_place:
                session.delete(amenityobj)
                session.commit()
            session.delete(placetodelete)
            session.commit()
            return placetodelete
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
