"""Module containing entities or classes for HBnB project"""
from uuid import uuid4
from datetime import datetime
import json


class Validator:
    """The CLass for Validator Methods"""
    @staticmethod
    def validate_user_mail(email):
        """Validates user mail"""
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            users = data['User']
            for userdata in users.values():
                if userdata['email'] == email.lower():
                    return False
            return True

    @staticmethod
    def validate_user_by_id(userid):
        """Validates user by its id"""
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            users = data['User']
            if userid not in users:
                return False
        return True

    @staticmethod
    def validate_address(address):
        """Validate address by str"""
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            places = data['Place']
            for placedata in places.values():
                if placedata['address'].lower() == address.lower():
                    return False
        return True

    @staticmethod
    def validate_city(city: str):
        """Validates city by its id"""
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            cities = data['City']
            if city not in cities:
                return False
        return True

    @staticmethod
    def validate_country(country: str):
        """Function for validating a country"""
        with open('countries.json', 'r') as file:
            data = json.loads(file.read())
            if country.upper() not in data:
                return False
            return True

    @staticmethod
    def validate_city_in_country(city: str, country: str):
        """Validates city by its name and country name"""
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            cities = data["City"]
            for citya in cities.values():
                if citya['name'].lower() == city.lower() and citya['country'].lower() == country.lower():
                    return False
            return True

    @staticmethod
    def validate_user_place(user, place):
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            users = data['User']
            if user not in users:
                return False
            places = data['Place']
            if place not in places:
                return False
            ouruser = users[user]
            if place in ouruser["host_places"]:
                print("User can not add review for his/her own place")
                return False
            return True


class DataManager:
    """The DataManager class provides methods for managing database"""
    @staticmethod
    def save_new_item(item):
        """Function for saving a new item to the database"""
        datatype = type(item).__name__
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
        data[datatype][item.id] = item.__dict__
        with open('data.json', 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_host_place(userid, place):
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['host_places'].append(place)
        with open('data.json', 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_review(userid, place, reviewid):
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['reviews'].append(reviewid)
            place = data['Place'][place]
            place['reviews'].append(reviewid)
        with open('data.json', 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def initialize_file():
        """Function to initialize the file"""
        keys = ["City", "Place", "User", "Amenity", "Review"]
        try:
            with open('data.json', 'r') as file:
                data = file.read()
                if any(data):
                    data = json.loads(data)
                else:
                    data = dict()
            for item in keys:
                if item not in data:
                    data[item] = dict()
            with open('data.json', 'w') as file:
                file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            with open('data.json', 'w') as file:
                data = dict()
                for item in keys:
                    data[item] = dict()
                file.write(json.dumps(data, indent=4))


class User:
    """The User Class"""
    def __init__(self, email: str, password: str, first_name: str, last_name: str):
        if Validator.validate_user_mail(email):
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
            print("User with this email already exists")


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


if __name__ == '__main__':
    DataManager.initialize_file()
    # Bak = City("Baku", "Az")
    # User1 = User("samir@gmail.com", "password", "Samir", "Ibrahim")
    # place1 = Place("Kazimin Mekani", "Gozel yer", "Bineqedi no 26", "341941b3-c4dc-4548-bf75-c801134cdb94", 3.45, 4.57, "69cf24f2-4aa4-4129-b1e5-2bc8f5ea3859", 5, 3, 45, 4)
    # User2 = User("memmed2gmail.com", "1234", "Memmed", "Sultanov")
    # review1 = Review("Gozel yerdi", 4.5, "f1dd8b69-dcfb-4b92-b31a-7db7de0ffc9e", "8a393759-9a3e-4916-8c90-596c8e2c006d")

