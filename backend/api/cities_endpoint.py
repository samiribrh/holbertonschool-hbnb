"""Module for user endpoint"""
from services.DataManipulation.datamanager import DataManager
from services.DataManipulation.crud import Crud
from services.Validators.validators import Validator
from services.Database.database import get_session
from model.city import City
from flask import Blueprint, jsonify, request
from uuid import uuid4

cities_bp = Blueprint('cities', __name__)


@cities_bp.get('/')
def get_cities():
    raw_data = Crud.get('City')
    data_dict = dict()
    for data in raw_data:
        data_dict.update(DataManager.custom_encoder(data))
    if not data_dict:
        return jsonify({'message': 'No cities found'}), 200
    return jsonify(data_dict), 200


@cities_bp.get('/<city_id>')
def get_city_by_id(city_id):
    raw_data = Crud.get('City', city_id)
    if not raw_data:
        return jsonify({'message': 'City not found'}), 404
    rd_data = DataManager.custom_encoder(raw_data)
    data_dict = dict()
    data_dict.update(rd_data)
    return jsonify(data_dict), 200


@cities_bp.post('/')
def create_city():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    name = data.get('name')
    country = data.get('country')
    if not (name and country):
        return jsonify({'error': 'Missing data'}), 400
    try:
        new_city_id = str(uuid4())
        city = City(id=new_city_id, name=name, country=country)
        DataManager.save_to_db(city)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    city = Crud.get('City', new_city_id)
    return jsonify(DataManager.custom_encoder(city)), 201


@cities_bp.put('/<city_id>')
def update_city(city_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    session = get_session()
    data = session.query(City).filter(City.id == city_id).all()
    if data is None:
        return jsonify({'error': 'City not found'}), 404
    name = datatoupdate.get('name')
    country = datatoupdate.get('country')
    if not (name and country):
        return jsonify({'error': 'Missing data'}), 400
    if Validator.validate_city_in_country(name, country):
        return jsonify({'error': 'City already exists'}), 400
    try:
        setattr(data[0], 'name', datatoupdate.get('name'))
        setattr(data[0], 'country', datatoupdate.get('country'))
        session.commit()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()
    return jsonify({'message': 'City updated'}), 201


@cities_bp.delete('/<city_id>')
def delete_city(city_id):
    if not city_id:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.delete('City', city_id)
    if status == 404:
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'message': 'City deleted'}), 204
