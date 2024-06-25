"""Module for CRUD operations."""
from Services.DataManipulation.datamanager import DataManager
from Model.amenity import Amenity
from Model.city import City
from Model.country import Country
from Model.place import Place
from Model.review import Review
from env.env import datafile
import json


class Crud:
    @staticmethod
    def get(entity_id, entity_type):
        """Method to get data"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            return data[entity_type][entity_id]

    @staticmethod
    def update(entity_id, entity_type, newdata):
        """Method to update data"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            data[entity_type][entity_id] = newdata
            DataManager.save_to_file(data, datafile)

    @staticmethod
    def delete(entity_id, entity_type):
        """Method to delete data"""
        eval(entity_type).delete(entity_id)
