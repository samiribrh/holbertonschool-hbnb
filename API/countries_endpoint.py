"""Module for user endpoint"""
from Services.DataManipulation.crud import Crud
from Model.country import Country
from env.env import countryfile, datafile
from flask import Blueprint, jsonify
import json

countries_bp = Blueprint('countries', __name__)


@countries_bp.route('/', methods=['GET'])
def get_countries():
    with open(countryfile, 'r') as file:
        countries = json.loads(file.read())
        return jsonify(countries), 200


@countries_bp.route('/<country_code>', methods=['GET'])
def get_country(country_code):
    with open(countryfile, 'r') as file:
        countries = json.loads(file.read())
        country = countries.get(country_code)
        if country is None:
            return jsonify({'error': 'No country found'}), 404
        return jsonify(country), 200


@countries_bp.route('/<country_code>/cities', methods=['GET'])
def get_cities(country_code):
    with open(countryfile, 'r') as file:
        countries = json.loads(file.read())
        if country_code not in countries:
            return jsonify({'error': 'No country found'}), 404
    with open(datafile, 'r') as file:
        data = json.loads(file.read())
        cities = data['City']
        cities_dict = dict()
        for city, info in cities.items():
            if info['country'] == country_code:
                cities_dict[city] = cities[city]
    return jsonify(cities_dict), 200
