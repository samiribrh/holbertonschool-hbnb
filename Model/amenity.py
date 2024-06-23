"""Module containing Amenity class"""
from Services.Validators.validators import *
from Services.datamanager import DataManager
from env.env import datafile
from uuid import uuid4
from datetime import datetime


class Amenity:
    """The Amenity Class"""
    def __init__(self, name: str):
        if Validator.validate_amenity(name):
            self.id = str(uuid4())
            self.name = name.lower()
            self.created_at = datetime.now().isoformat()
            self.updated_at = datetime.now().isoformat()
            DataManager.save_new_item(self)
        else:
            print("Amenity already exists")

    @staticmethod
    def delete(amenityid):
        """Function to delete a Amenity from the database"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            del data['Amenity'][amenityid]
            DataManager.save_to_file(data, datafile)
        return data
