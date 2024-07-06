"""Module for CRUD operations."""
from Services.DataManipulation.datamanager import DataManager
from Services.database import get_session
from Model.amenity import Amenity
from Model.city import City
from Model.country import Country
from Model.place import Place
from Model.review import Review
from Model.user import User
from Model.place_amenity import PlaceAmenity
from env.env import datafile
from datetime import datetime
import json


class Crud:
    @staticmethod
    def get(entity_type, entity_id=None):
        """Method to get data"""
        session = get_session()
        try:
            if entity_id is None:
                return session.query(eval(entity_type)).all()
            data = session.query(eval(entity_type)).filter(eval(entity_type).id == entity_id).one()
            if not data:
                return None
            return data
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update(entity_type, entity_id, column_name, new_data):
        """Method to update data"""
        session = get_session()
        try:
            entity = session.query(eval(entity_type)).filter_by(id=entity_id).one()
            setattr(entity, column_name, new_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(entity_type, entity_id):
        """Method to delete data"""
        session = get_session()
        try:
            entity = session.query(eval(entity_type)).filter_by(id=entity_id).one()
            session.delete(entity)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
