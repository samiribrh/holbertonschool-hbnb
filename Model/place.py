"""Module containing Place class"""
from Services.Validators.validators import *
from Services.DataManipulation.datamanager import DataManager
from Model.review import Review
from env.env import datafile
from uuid import uuid4
from datetime import datetime


class Place:
    """The Place Class"""

    def __init__(self, name: str, description: str, address: str, city: str, latitude: float, longitude: float,
                 host: str, num_of_rooms: int, bathrooms: int, price: float, max_guests: int):
        """Place constructor"""
        if Validator.validate_address(address):
            if Validator.validate_city(city):
                if Validator.validate_user_by_id(host):
                    self.id = str(uuid4())
                    self.name = name.capitalize()
                    self.description = description
                    self.address = address
                    self.city = city
                    self.latitude = latitude
                    self.longitude = longitude
                    self.host = host
                    self.num_of_rooms = num_of_rooms
                    self.bathrooms = bathrooms
                    self.price = price
                    self.max_guests = max_guests
                    self.amenities = []
                    self.reviews = []
                    self.created_at = datetime.now().isoformat()
                    self.updated_at = datetime.now().isoformat()
                    DataManager.save_new_item(self)
                    DataManager.add_host_place(self.host, self.id)
                else:
                    print("Host not found")
            else:
                print("City not valid")
        else:
            print("Place with this address already already exists")

    @staticmethod
    def delete(deletionid):
        """Function to delete a Place from the database"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
        reviews = data['Place'][deletionid]['reviews']
        for review in reviews:
            Review.delete(review)
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
        places = data['Place']
        hostid = places[deletionid]['host']
        del places[deletionid]
        hostuser = data['User'][hostid]
        if deletionid in hostuser['host_places']:
            hostuser['host_places'].remove(deletionid)
        DataManager.save_to_file(data, datafile)
        return data
