"""Module containing DataManager class"""
from services.Database.database import get_session


class DataManager:
    """The DataManager class provides methods for managing database"""

    @staticmethod
    def custom_encoder(obj):
        """Method to turn object into json format"""
        obj_dict = obj.__dict__
        obj_id = obj_dict.get('id')
        obj_dict.pop('_sa_instance_state')
        return {obj_id: obj_dict}

    @staticmethod
    def save_to_db(newdata):
        """Method to save data to database"""
        session = get_session()
        try:
            session.add(newdata)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def add_amenity_to_place(user: str, amenity: str, place: str):
        """Method for adding an amenity to a place"""
        from services.Validators.validators import Validator

        session = get_session()
        try:
            if not Validator.validate_user_owns_place(user, place):
                raise ValueError("User does not own place")
            if Validator.validate_amenity_in_place(amenity, place):
                raise ValueError("Amenity already exists in place")
            from model.place_amenity import PlaceAmenity
            new_pl_am = PlaceAmenity(place_id=place, amenity_id=amenity)
            DataManager.save_to_db(new_pl_am)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
