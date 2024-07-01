"""Module containing Amenity class"""
from Services.Validators.validators import *
from Services.DataManipulation.datamanager import DataManager
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
            raise ValueError("Amenity already exists")

    @staticmethod
    def delete(amenityid):
        """Function to delete a Amenity from the database"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            del data['Amenity'][amenityid]
            places = data['Place']
            for place in places.values():
                if any(place['amenities']) and amenityid in place['amenities']:
                    place['amenities'].remove(amenityid)
            DataManager.save_to_file(data, datafile)
        return data
