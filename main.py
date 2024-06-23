"""Module containing entities or classes for HBnB project"""
from classes import *
from validators import *


class DataManager:
    """The DataManager class provides methods for managing database"""

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
    def add_host_place(userid: str, place: str):
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['host_places'].append(place)
        with open('data.json', 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_review(userid: str, place: str, reviewid: str):
        with open('data.json', 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['reviews'].append(reviewid)
            place = data['Place'][place]
            place['reviews'].append(reviewid)
        with open('data.json', 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_amenity_to_place(user: str, amenity: str, place: str):
        """Function for adding an amenity to a place"""
        if not Validator.validate_user_owns_place(user, place):
            if Validator.check_amenity_in_place(amenity, place):
                with open('data.json', 'r') as file:
                    data = json.loads(file.read())
                    place = data['Place'][place]
                    amenities = data['Amenity']
                    for amntdata in amenities.values():
                        if amntdata['name'] == amenity:
                            amenity = amntdata['id']
                            break
                    place['amenities'].append(amenity)
                with open('data.json', 'w') as file:
                    file.write(json.dumps(data, indent=4))
            else:
                print("Amenity already exists in specified place")
        else:
            print("User does not own this place")


if __name__ == '__main__':
    DataManager.initialize_file()
