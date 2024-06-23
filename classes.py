import json
from uuid import uuid4
from datetime import datetime
from main import filename, countryfile, DataManager
from validators import *


class User:
    """The User Class"""
    def __init__(self, email: str, password: str, first_name: str, last_name: str):
        mailcheck, status = Validator.validate_user_mail(email)
        if mailcheck:
            self.id = str(uuid4())
            self.email = email.lower()
            self.password = password
            self.first_name = first_name.capitalize()
            self.last_name = last_name.capitalize()
            self.host_places = []
            self.reviews = []
            self.created_at = datetime.now().isoformat()
            self.updated_at = datetime.now().isoformat()
            DataManager.save_new_item(self)
        else:
            if status == 1:
                print("Email format is not correct")
            else:
                print("User with this email already exists")

    @staticmethod
    def delete(deletionid):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        user = data['User'][deletionid]
        hostplaces = user['host_places']
        reviews = user['reviews']
        for review in reviews:
            data = Review.delete(review)
        DataManager.save_to_file(data, filename)
        for hostplace in hostplaces:
            data = Place.delete(hostplace)
        DataManager.save_to_file(data, filename)
        del data['User'][deletionid]
        DataManager.save_to_file(data, filename)
        return data


class Place:
    """The Place Class"""
    def __init__(self, name: str, description: str, address: str, city: str, latitude: float, longitude: float,
                 host: str, num_of_rooms: int, bathrooms: int, price: float, max_guests: int):
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
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        reviews = data['Place'][deletionid]['reviews']
        for review in reviews:
            Review.delete(review)
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        places = data['Place']
        hostid = places[deletionid]['host']
        del places[deletionid]
        hostuser = data['User'][hostid]
        if deletionid in hostuser['host_places']:
            hostuser['host_places'].remove(deletionid)
        DataManager.save_to_file(data, filename)
        return data


class Review:
    """The Review Class"""
    def __init__(self, feedback: str, rating: float, user: str, place: str):
        if Validator.validate_user_by_id(user):
            if Validator.validate_user_place(user, place):
                self.id = str(uuid4())
                self.feedback = feedback
                self.rating = rating
                self.user = user
                self.place = place
                self.created_at = datetime.now().isoformat()
                self.updated_at = datetime.now().isoformat()
                DataManager.save_new_item(self)
                DataManager.add_review(self.user, self.place, self.id)
            else:
                print("Place not valid")
        else:
            print("User not valid")

    @staticmethod
    def delete(deletionid):
        """Function to delete a Review from the database"""
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            reviews = data['Review']
            revowner = reviews[deletionid]['user']
            placeid = reviews[deletionid]['place']
            data['Place'][placeid]['reviews'].remove(deletionid)
            data['User'][revowner]['reviews'].remove(deletionid)
            del reviews[deletionid]
            DataManager.save_to_file(data, filename)
        return data


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
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            del data['Amenity'][amenityid]
            DataManager.save_to_file(data, filename)
        return data


class Country:
    """The Country Class"""
    def __init__(self, id: str, name: str):
        """Initialization of Country Instance"""
        self.id = id
        self.name = name
        DataManager.save_new_item(self)


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
                print('City already exists')
        else:
            print("Country is not valid")

    @staticmethod
    def delete(cityid):
        """Function to delete a City from the database"""
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            places = data['Place']
            for place in places.values():
                if place['city'] == cityid:
                    data = Place.delete(place['id'])
            del data['City'][cityid]
            DataManager.save_to_file(data, filename)
        return data


