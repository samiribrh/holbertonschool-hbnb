"""Module containing City class"""
from Services.Validators.validators import *
from Services.DataManipulation.datamanager import DataManager
from Model.place import Place
from env.env import datafile
from uuid import uuid4
from datetime import datetime


class City:
    """The City Class"""
    def __init__(self, name: str, country: str):
        """Initialization of City Instance"""
        if Validator.validate_country(country):
            if Validator.validate_city_in_country(name, country):
                self.id = str(uuid4())
                self.name = ' '.join(word.capitalize() for word in name.split())
                self.country = country.upper()
                self.created_at = datetime.now().isoformat()
                self.updated_at = datetime.now().isoformat()
                DataManager.save_new_item(self)
            else:
                raise ValueError("City already exists")
        else:
            raise ValueError('Invalid country value')

    @staticmethod
    def delete(cityid):
        """Function to delete a City from the database"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            places = data['Place']
            for place in places.values():
                if place['city'] == cityid:
                    data = Place.delete(place['id'])
            del data['City'][cityid]
            DataManager.save_to_file(data, datafile)
        return data
