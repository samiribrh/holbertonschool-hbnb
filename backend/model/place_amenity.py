"""Module containing place amenity junction model."""
from services.Validators.validators import Validator
from services.Database.database import Base, get_session
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import validates
from datetime import datetime
from uuid import uuid4


class PlaceAmenity(Base):
    """Class representing a place amenity junction table."""
    __tablename__ = 'place_amenity'

    id = Column(String(36), primary_key=True, default=lambda: uuid4())
    place_id = Column(String(36), nullable=False)
    amenity_id = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    @validates('place_id')
    def validate_place_id(self, key, value):
        validated_place = value.lower()
        if not Validator.validate_place(validated_place):
            raise ValueError("Place is not valid")
        return validated_place

    @validates('amenity_id')
    def validate_amenity_id(self, key, value):
        validated_amenity = value.lower()
        if not Validator.validate_amenity(validated_amenity):
            raise ValueError("Amenity is not valid")
        return validated_amenity

    @staticmethod
    def delete(deletionid: str):
        """Delete a place amenity junction column."""
        session = get_session()
        try:
            columntodelete = session.query(PlaceAmenity).filter(PlaceAmenity.id == deletionid).one()
            if not columntodelete:
                raise ValueError("Column does not exist")
            session.delete(columntodelete)
            session.commit()
            return columntodelete
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
