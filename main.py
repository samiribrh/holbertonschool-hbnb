"""Module containing entities or classes for HBnB project"""
from uuid import uuid4
from datetime import datetime
import json


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
        if User.validate_user_mail(email):
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

    @staticmethod
    def validate_user_mail(email):
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            users = data['User']
            for userdata in users.values():
                if userdata['email'] == email.lower():
                    return False
            return True


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
        if City.validate_country(country):
            if City.validate_city(name, country):
                self.id = str(uuid4())
                self.name = ' '.join(word.capitalize() for word in name.split())
                self.country = country.upper()
                self.created_at = datetime.now().isoformat()
                DataManager.save_new_item(self)
            else:
                print('City already exists')
        else:
            print("Country is not valid")

    @staticmethod
    def validate_country(country: str):
        """Function for validating a country"""
        with open('countries.json', 'r') as file:
            data = json.loads(file.read())
            if country.upper() not in data:
                return False
            return True

    @staticmethod
    def validate_city(city: str, country: str):
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            cities = data["City"]
            for citya in cities.values():
                if citya['name'].lower() == city.lower() and citya['country'].lower() == country.lower():
                    return False
            return True


if __name__ == '__main__':
    DataManager.initialize_file()

