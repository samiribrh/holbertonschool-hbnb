"""Module containing DataManager class"""
from env.env import datafile
from Services.Validators.validators import *
import json


class DataManager:
    """The DataManager class provides methods for managing database"""
    @staticmethod
    def save_to_file(data, datafile):
        """Method to save data to file"""
        with open(datafile, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def save_new_item(item):
        """Function for saving a new item to the database"""
        datatype = type(item).__name__
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
        data[datatype][item.id] = item.__dict__
        with open(datafile, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_host_place(userid: str, place: str):
        """Method to add his host place to the user data"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['host_places'].append(place)
        with open(datafile, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_review(userid: str, place: str, reviewid: str):
        """Method to add review"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            user = data['User'][userid]
            user['reviews'].append(reviewid)
            place = data['Place'][place]
            place['reviews'].append(reviewid)
        with open(datafile, 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def add_amenity_to_place(user: str, amenity: str, place: str):
        """Method for adding an amenity to a place"""
        if not Validator.validate_user_owns_place(user, place):
            if Validator.check_amenity_in_place(amenity, place):
                with open(datafile, 'r') as file:
                    data = json.loads(file.read())
                    place = data['Place'][place]
                    amenities = data['Amenity']
                    for amntdata in amenities.values():
                        if amntdata['name'] == amenity:
                            amenity = amntdata['id']
                            break
                    place['amenities'].append(amenity)
                with open(datafile, 'w') as file:
                    file.write(json.dumps(data, indent=4))
            else:
                print("Amenity already exists in specified place")
        else:
            print("User does not own this place")
