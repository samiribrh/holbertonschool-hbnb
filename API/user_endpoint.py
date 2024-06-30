"""Module for user endpoint"""
from Services.DataManipulation.crud import Crud
from Model.user import User
from flask import Blueprint, jsonify, request

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
def get_users():
    data = Crud.get('User')
    for spec in data.values():
        spec.pop('password')
    return jsonify(data)


@users_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    data = Crud.get('User', user_id)
    if data is None:
        return jsonify({'error': 'User not found'}), 404
    data.pop('password')
    return jsonify(data)


@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if not email or not password or not first_name or not last_name:
        return jsonify({'error': 'Missing data'}), 400
    try:
        user = User(email, password, first_name, last_name)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(user.__dict__), 201


@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('User', user_id)
    data['email'] = datatoupdate.get('email')
    data['password'] = datatoupdate.get('password')
    data['first_name'] = datatoupdate.get('first_name')
    data['last_name'] = datatoupdate.get('last_name')
    if not (data['email'] and data['password'] and data['first_name'] and data['last_name']):
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.update(user_id, 'User', data)
    if status == 404:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User updated'}), 201


@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not user_id:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.delete(user_id, 'User')
    if status == 404:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 204
