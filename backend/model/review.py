"""Module for Review Class"""
from services.Validators.validators import Validator
from services.Database.database import Base, get_session
from sqlalchemy import Column, String, Float, Text, DateTime
from sqlalchemy.orm import validates
from datetime import datetime
from uuid import uuid4


class Review(Base):
    """The Review Class"""
    __tablename__ = 'reviews'

    id = Column(String(36), primary_key=True, default=lambda: uuid4())
    rating = Column(Float, nullable=False)
    feedback = Column(Text)
    user = Column(String(36), nullable=False)
    place = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)

    @validates('rating')
    def validate_rating(self, key, value):
        if value > 5 or value < 0:
            raise ValueError("Rating must be between 0 and 5")
        return value

    @validates('user')
    def validate_user(self, key, value):
        validated_user = value.lower()
        if not Validator.validate_user_by_id(validated_user):
            raise ValueError("User is not valid")
        return validated_user

    @validates('place')
    def validate_place(self, key, value):
        validated_place = value.lower()
        if not Validator.validate_place(value):
            raise ValueError("Place is not valid")
        if Validator.validate_user_owns_place(self.user, validated_place):
            raise ValueError("Place can not be reviewed by host user")
        return validated_place

    @staticmethod
    def delete(deletionid: str):
        """Function to delete a Review from the database"""
        session = get_session()
        try:
            reviewtodelete = session.query(Review).filter(id == deletionid).first()
            if not reviewtodelete:
                raise ValueError("Review does not exist")
            session.delete(reviewtodelete)
            session.commit()
            return reviewtodelete
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
