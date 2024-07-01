"""Module Containing Services for Model"""
from env.env import datafile, countryfile
import json
import re


class Validator:
    """The CLass for Validator Methods"""
    @staticmethod
    def is_positive_int(value):
        """Validates the value is a positive integer"""
        if not isinstance(value, int):
            return False
        if value < 0:
            return False
        return True

    @staticmethod
    def validate_user_mail(email: str):
        """Validates user mail"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email) is not None:
            with open(datafile, 'r') as file:
                data = json.loads(file.read())
                users = data['User']
                for userdata in users.values():
                    if userdata['email'] == email.lower():
                        return False, 0
                return True, 0
        return False, 1

    @staticmethod
    def validate_user_by_id(userid: str):
        """Validates user by its id"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            users = data['User']
            if userid not in users:
                return False
        return True

    @staticmethod
    def validate_address(address: str):
        """Validate address by str"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            places = data['Place']
            for placedata in places.values():
                if placedata['address'].lower() == address.lower():
                    return False
        return True

    @staticmethod
    def validate_city(city: str):
        """Validates city by its id"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            cities = data['City']
            if city not in cities:
                return False
        return True

    @staticmethod
    def validate_country(country: str):
        """Function for validating a country"""
        with open(countryfile, 'r') as file:
            data = json.loads(file.read())
            if country.upper() not in data:
                return False
            return True

    @staticmethod
    def validate_city_in_country(city: str, country: str):
        """Validates city by its name and country name"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            cities = data["City"]
            for citya in cities.values():
                if citya['name'].lower() == city.lower() and citya['country'].lower() == country.lower():
                    return False
            return True

    @staticmethod
    def validate_coordinates(latitude: float, longitude: float):
        """Validates latitude and longitude"""
        if latitude < -90 or latitude > 90:
            return False
        if longitude < -180 or longitude > 180:
            return False
        return True

    @staticmethod
    def validate_user_place(user: str, place: str):
        """Validates user place"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            users = data['User']
            if user not in users:
                return False
            places = data['Place']
            if place not in places:
                return False
            ouruser = users[user]
            if place in ouruser["host_places"]:
                return False
            return True

    @staticmethod
    def validate_user_owns_place(user: str, place: str):
        """Function for validating user owns place"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            ouruser = data['User'][user]
            if place in ouruser["host_places"]:
                return False
            return True

    @staticmethod
    def validate_amenity(amenity: str):
        """If amenity not exists return true"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            amenities = data['Amenity']
            for amenitydata in amenities.values():
                if amenitydata['name'] == amenity.lower():
                    return False
            return True

    @staticmethod
    def check_valid_amenity(amenity: str):
        """Function for validating amenity"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            amenities = data['Amenity']
            if amenity not in amenities:
                return False
            return True

    @staticmethod
    def check_amenity_in_place(amenity: str, place: str):
        """Function for validating amenity inside place"""
        with open(datafile, 'r') as file:
            data = json.loads(file.read())
            ourplace = data['Place'][place]
            if amenity in ourplace['amenities']:
                return False
        return True
