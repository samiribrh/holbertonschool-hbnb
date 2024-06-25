"""Module for Review Class"""
from Services.Validators.validators import *
from Services.DataManipulation.datamanager import DataManager
from env.env import datafile
from uuid import uuid4
from datetime import datetime


class Review:
    """The Review Class"""
    def __init__(self, feedback: str, rating: float, user: str, place: str):
        """Review Class constructor"""
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
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            reviews = data['Review']
            revowner = reviews[deletionid]['user']
            placeid = reviews[deletionid]['place']
            data['Place'][placeid]['reviews'].remove(deletionid)
            data['User'][revowner]['reviews'].remove(deletionid)
            del reviews[deletionid]
            DataManager.save_to_file(data, datafile)
        return data
