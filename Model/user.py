"""Module for User class"""
from Services.Validators.validators import *
from Model.review import Review
from Model.place import Place
from Services.DataManipulation.datamanager import DataManager
from uuid import uuid4
from datetime import datetime
from env.env import datafile


class User:
    """The User Class"""
    def __init__(self, email: str, password: str, first_name: str, last_name: str, is_admin=False):
        """User class constructor"""
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
            self.is_admin = is_admin
            DataManager.save_new_item(self)
        else:
            if status == 1:
                raise ValueError("Email format is not correct")
            else:
                raise ValueError("User with this email already exists")

    @staticmethod
    def delete(deletionid):
        """Method for deleting a user"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
        user = data['User'][deletionid]
        hostplaces = user['host_places']
        reviews = user['reviews']
        for review in reviews:
            data = Review.delete(review)
        DataManager.save_to_file(data, datafile)
        for hostplace in hostplaces:
            data = Place.delete(hostplace)
        DataManager.save_to_file(data, datafile)
        del data['User'][deletionid]
        DataManager.save_to_file(data, datafile)
        return data
