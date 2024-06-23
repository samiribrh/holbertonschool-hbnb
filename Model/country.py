"""Module containing Country class"""
from Services.datamanager import DataManager


class Country:
    """The Country Class"""
    def __init__(self, id: str, name: str):
        """Country constructor"""
        self.id = id
        self.name = name
        DataManager.save_new_item(self)
