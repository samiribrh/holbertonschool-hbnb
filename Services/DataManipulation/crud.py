"""Module for CRUD operations."""
from Services.DataManipulation.datamanager import DataManager
from Model.amenity import Amenity
from Model.city import City
from Model.country import Country
from Model.place import Place
from Model.review import Review
from Model.user import User
from env.env import datafile
from datetime import datetime
import json


class Crud:
    @staticmethod
    def get(entity_type, entity_id=None):
        """Method to get data"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            if entity_id is None:
                return data[entity_type]
            if entity_id not in data[entity_type]:
                return None
            return data[entity_type][entity_id]

    @staticmethod
    def update(entity_id, entity_type, newdata):
        """Method to update data"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            if entity_id not in data[entity_type]:
                return 404
            data[entity_type][entity_id] = newdata
            data[entity_type][entity_id]['updated_at'] = datetime.now().isoformat()
            DataManager.save_to_file(data, datafile)

    @staticmethod
    def delete(entity_id, entity_type):
        """Method to delete data"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
        if entity_id not in data[entity_type]:
            return 404
        eval(entity_type).delete(entity_id)
        return 204
