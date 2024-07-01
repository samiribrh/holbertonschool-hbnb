"""Module containing Place class"""
from Services.Validators.validators import *
from Services.Validators.exceptions import (HostNotFound, CityNotFound,
                                            PlaceAlreadyExistsError, AmenityNotFound,
                                            ValidNumberError)
from Services.DataManipulation.datamanager import DataManager
from Model.review import Review
from env.env import datafile
from uuid import uuid4
from datetime import datetime


class Place:
    """The Place Class"""

    def __init__(self, name: str, description: str, address: str, city: str, latitude: float, longitude: float,
                 host: str, num_of_rooms: int, bathrooms: int, price: float, max_guests: int, amenities=None):
        """Place constructor"""
        if amenities is None:
            amenities = []
        for amenity in amenities:
            if not Validator.check_valid_amenity(amenity):
                raise AmenityNotFound("Amenity Not Found")
        if not Validator.validate_coordinates(latitude, longitude):
            raise ValueError("Latitude and Longitude are not valid")
        if not (Validator.is_positive_int(num_of_rooms), Validator.is_positive_int(bathrooms),
                Validator.is_positive_int(max_guests)):
            raise ValidNumberError("num_of_rooms, bathrooms, max_guests should be positive integers")
        if not ((isinstance(price, int) or isinstance(price, float)) and (price >= 0)):
            raise ValidNumberError("Price should be positive integer")
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
                    self.amenities = amenities
                    self.reviews = []
                    self.created_at = datetime.now().isoformat()
                    self.updated_at = datetime.now().isoformat()
                    DataManager.save_new_item(self)
                    DataManager.add_host_place(self.host, self.id)
                else:
                    raise HostNotFound("Host not found")
            else:
                raise CityNotFound("City not valid")
        else:
            raise PlaceAlreadyExistsError("Place with this address already exists")

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
