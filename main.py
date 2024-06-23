"""Module containing entities or classes for HBnB project"""
from classes import *
from validators import *
filename = 'data.json'
countryfile = 'countries.json'
import json


class DataManager:
    """The DataManager class provides methods for managing database"""

    @staticmethod
    def initialize_file():
        """Function to initialize the file"""
        keys = ["City", "Place", "User", "Amenity", "Review"]
        try:
            with open(filename, 'r') as file:
                data = file.read()
                if any(data):
                    data = json.loads(data)
                else:
                    data = dict()
            for item in keys:
                if item not in data:
                    data[item] = dict()
            with open(filename, 'w') as file:
                file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            with open(filename, 'w') as file:
                data = dict()
                for item in keys:
                    data[item] = dict()
                file.write(json.dumps(data, indent=4))

    @staticmethod
    def save_to_file(data, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def save_new_item(item):
        """Function for saving a new item to the database"""
        datatype = type(item).__name__
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        data[datatype][item.id] = item.__dict__
        with open(filename, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_host_place(userid: str, place: str):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['host_places'].append(place)
        with open(filename, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_review(userid: str, place: str, reviewid: str):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['reviews'].append(reviewid)
            place = data['Place'][place]
            place['reviews'].append(reviewid)
        with open(filename, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_amenity_to_place(user: str, amenity: str, place: str):
        """Function for adding an amenity to a place"""
        if not Validator.validate_user_owns_place(user, place):
            if Validator.check_amenity_in_place(amenity, place):
                with open(filename, 'r') as file:
                    data = json.loads(file.read())
                    place = data['Place'][place]
                    amenities = data['Amenity']
                    for amntdata in amenities.values():
                        if amntdata['name'] == amenity:
                            amenity = amntdata['id']
                            break
                    place['amenities'].append(amenity)
                with open(filename, 'w') as file:
                    file.write(json.dumps(data, indent=4))
            else:
                print("Amenity already exists in specified place")
        else:
            print("User does not own this place")

    @staticmethod
    def get(entity_id, entity_type):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            return data[entity_type][entity_id]

    @staticmethod
    def update(entity):
        pass

    @staticmethod
    def delete(entity_id, entity_type):
        eval(entity_type).delete(entity_id)


if __name__ == '__main__':
    DataManager.initialize_file()
    with open('datacopy.json', 'r') as file:
        data = json.loads(file.read())
    with open('data.json', 'w') as file:
        file.write(json.dumps(data, indent=4))
    DataManager.delete("a2562180-7f8a-45b5-b369-1af2d60e6695", "City")
