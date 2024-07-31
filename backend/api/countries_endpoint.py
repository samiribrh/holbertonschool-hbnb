"""Module for user endpoint"""
from services.DataManipulation.datamanager import DataManager
from services.DataManipulation.crud import Crud
from services.Database.database import get_session
from model.country import Country
from model.city import City
from flask import Blueprint, jsonify

countries_bp = Blueprint('countries', __name__)


@countries_bp.get('/')
def get_countries():
    raw_data = Crud.get('Country')
    data_dict = dict()
    for data in raw_data:
        data_dict.update(DataManager.custom_encoder(data))
    if not data_dict:
        return jsonify({'message': 'No countries found'})
    return jsonify(data_dict), 200


@countries_bp.get('/<country_code>')
def get_country(country_code):
    raw_data = Crud.get('Country', country_code)
    if not raw_data:
        return jsonify({'message': 'Country not found'}), 404
    rd_data = DataManager.custom_encoder(raw_data)
    data_dict = dict()
    data_dict.update(rd_data)
    return jsonify(data_dict), 200


@countries_bp.get('/<country_code>/cities')
def get_cities(country_code):
    session = get_session()
    country = session.query(Country).filter_by(id=country_code).all()
    if not country:
        return jsonify({'message': 'Country not found'}), 404
    raw_data = session.query(City).filter_by(country=country_code).all()
    data_dict = dict()
    for data in raw_data:
        rd_data = DataManager.custom_encoder(data)
        data_dict.update(rd_data)
    if not data_dict:
        return jsonify({'message': 'No cities found'}), 404
    return jsonify(data_dict), 200
