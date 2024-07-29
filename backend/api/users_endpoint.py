"""Module for user endpoint"""
from services.DataManipulation.datamanager import DataManager
from services.DataManipulation.crud import Crud
from services.database import get_session
from model.user import User
from model.review import Review
from flask import Blueprint, jsonify, request
from uuid import uuid4

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
def get_users():
    raw_data = Crud.get('User')
    data_dict = dict()
    for data in raw_data:
        rd_data = DataManager.custom_encoder(data)
        for key, value in rd_data.items():
            value.pop('password')
        data_dict.update(rd_data)
    if not data_dict:
        return jsonify({'message': 'No users found'}), 200
    return jsonify(data_dict), 200


@users_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    raw_data = Crud.get('User', user_id)
    if raw_data is None:
        return jsonify({'error': 'User not found'}), 404
    rd_data = DataManager.custom_encoder(raw_data)
    for key, value in rd_data.items():
        value.pop('password')
    data_dict = dict()
    data_dict.update(rd_data)
    return jsonify(data_dict), 200


@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role')
    if not (email and password and first_name and last_name):
        return jsonify({'error': 'Missing data'}), 400
    try:
        new_user_id = str(uuid4())
        new_user = User(id=new_user_id, email=email, password=password,
                        first_name=first_name, last_name=last_name, role=role)
        DataManager.save_to_db(new_user)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    user = Crud.get('User', new_user_id)
    return jsonify(DataManager.custom_encoder(user)), 201


@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('User', user_id)
    if data is None:
        return jsonify({'error': 'User not found'}), 404
    fields_to_update = ['email', 'password', 'first_name', 'last_name', 'role']
    for field in fields_to_update:
        if datatoupdate.get(field):
            try:
                status = Crud.update('User', user_id, field, datatoupdate[field])
                if status == 404:
                    return jsonify({'error': 'User not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'User updated'}), 201


@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not user_id:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.delete('User', user_id)
    if status == 404:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 204


@users_bp.route('/<user_id>/reviews', methods=['GET'])
def get_reviews(user_id):
    if not user_id:
        return jsonify({'error': 'Missing data'}), 400
    session = get_session()
    try:
        reviews = session.query(Review).filter(Review.user == user_id).all()
        data_dict = dict()
        for data in reviews:
            rd_data = DataManager.custom_encoder(data)
            data_dict.update(rd_data)
        if not data_dict:
            return jsonify({'message': 'No users found'}), 200
        return jsonify(data_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 200
    finally:
        session.close()
