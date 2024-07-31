"""Module Containing services for model"""
from services.Database.database import get_session


class Validator:
    """The CLass for Validator Methods"""
    @staticmethod
    def is_positive_int(value):
        """Validates the value is a positive integer"""
        if not isinstance(value, int):
            return False
        if value < 0:
            return False
        return True

    @staticmethod
    def validate_user_mail(email: str):
        """Validates user mail"""
        import re

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email) is not None:
            from model.user import User
            session = get_session()
            try:
                users = session.query(User).filter(User.email == email).all()
                if users:
                    return False, 0
                return True, 0
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        return False, 1

    @staticmethod
    def validate_user_by_id(userid: str):
        """Validates user by its id"""
        from services.DataManipulation.crud import Crud

        user = Crud.get('User', userid)
        if not user:
            return False
        return True

    @staticmethod
    def validate_address(address: str):
        """Validate address by str"""
        from model.place import Place

        session = get_session()
        try:
            places = session.query(Place).filter(Place.address == address).all()
            if places:
                return False
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def validate_city(city: str):
        """Validates city by its id"""
        from services.DataManipulation.crud import Crud

        city = Crud.get('City', city)
        if not city:
            return False
        return True

    @staticmethod
    def validate_country(country: str):
        """Function for validating a country"""
        from services.DataManipulation.crud import Crud

        country = Crud.get('Country', country.upper())
        if not country:
            return False
        return True

    @staticmethod
    def validate_city_in_country(city: str, country: str):
        """Validates city by its name and country name"""
        from model.city import City

        session = get_session()
        try:
            cities = session.query(City).filter(City.country == country).all()
            for citydata in cities:
                if citydata.name == city:
                    return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def validate_place(place: str):
        """Validates if place exists"""
        from services.DataManipulation.crud import Crud

        place = Crud.get('Place', place)
        if not place:
            return False
        return True

    @staticmethod
    def validate_user_owns_place(user: str, place: str):
        """Function for validating user owns place"""
        from model.place import Place

        session = get_session()
        try:
            places = session.query(Place).filter(Place.host == user).all()
            for placedata in places:
                if placedata.id == place:
                    return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def validate_amenity(amenity: str):
        """Function for validating amenity"""
        from model.amenity import Amenity

        session = get_session()
        try:
            amenities = session.query(Amenity).filter(Amenity.id == amenity or Amenity.name == amenity).all()
            if amenities:
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def validate_amenity_in_place(amenity: str, place: str):
        """Function for validating amenity inside place"""
        from model.place_amenity import PlaceAmenity

        session = get_session()
        try:
            placeamenity = (session.query(PlaceAmenity)
                            .filter(PlaceAmenity.amenity_id == amenity, PlaceAmenity.place_id == place).all())
            if placeamenity:
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
