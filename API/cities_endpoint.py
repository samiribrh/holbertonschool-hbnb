"""Module for user endpoint"""
from Services.DataManipulation.crud import Crud
from Services.Validators.exceptions import CityAlreadyExistsError, InvalidCountryError
from Services.Validators.validators import Validator
from Model.city import City
from flask import Blueprint, jsonify, request

cities_bp = Blueprint('cities', __name__)


@cities_bp.route('/', methods=['GET'])
def get_cities():
    data = Crud.get('City')
    return jsonify(data), 200


@cities_bp.route('/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    data = Crud.get('City', city_id)
    if data is None:
        return jsonify({'error': 'City not found'}), 404
    return jsonify(data), 200


@cities_bp.route('/', methods=['POST'])
def create_city():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    name = data.get('name')
    country = data.get('country')
    if not name or not country:
        return jsonify({'error': 'Missing data'}), 400
    try:
        city = City(name, country)
    except CityAlreadyExistsError:
        return jsonify({'error': 'City already exists'}), 400
    except InvalidCountryError:
        return jsonify({'error': 'Invalid country'}), 400
    return jsonify(city.__dict__), 201


@cities_bp.route('/<city_id>', methods=['PUT'])
def update_city(city_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('City', city_id)
    if data is None:
        return jsonify({'error': 'City not found'}), 404
    if not Validator.validate_country(datatoupdate.get('country')):
        return jsonify({'error': 'Invalid country'}), 400
    data['name'] = datatoupdate.get('name')
    data['country'] = datatoupdate.get('country')
    if not (data['name'] or data['country']):
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.update(city_id, 'City', data)
    if status == 404:
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'message': 'City updated'}), 200


@cities_bp.route('/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    if not city_id:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.delete(city_id, 'City')
    if status == 404:
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'message': 'City deleted'}), 204
