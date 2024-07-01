"""Module for amenities endpoint"""
from Services.DataManipulation.crud import Crud
from Model.amenity import Amenity
from flask import Blueprint, jsonify, request

amenities_bp = Blueprint('amenities', __name__)


@amenities_bp.route('/', methods=['GET'])
def get_amenities():
    data = Crud.get('Amenity')
    return jsonify(data), 200


@amenities_bp.route('/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    data = Crud.get('Amenity', amenity_id)
    if data is None:
        return jsonify({'message': 'Amenity not found'}), 404
    return jsonify(data), 200


@amenities_bp.route('/', methods=['POST'])
def create_amenity():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Amenity name is required'}), 400
    try:
        amenity = Amenity(name)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(amenity.__dict__), 201


@amenities_bp.route('/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('Amenity', amenity_id)
    if data is None:
        return jsonify({'error': 'Amenity not found'}), 404
    data['name'] = datatoupdate.get('name')
    if not data['name']:
        return jsonify({'error': 'Amenity name is required'}), 400
    status = Crud.update(amenity_id, 'Amenity', data)
    if status == 404:
        return jsonify({'error': 'Amenity not found'}), 404
    return jsonify({'message': 'Amenity updated'}), 201


@amenities_bp.route('/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    if not amenity_id:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.delete(amenity_id, 'Amenity')
    if status == 404:
        return jsonify({'error': 'Amenity not found'}), 404
    return jsonify({'message': 'Amenity deleted'}), 204
