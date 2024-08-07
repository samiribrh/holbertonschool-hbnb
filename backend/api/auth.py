from model.user import User
from services.DataManipulation.datamanager import DataManager
from services.DataManipulation.crud import Crud
from services.Database.database import get_session
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash
from uuid import uuid4

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/register')
def register():
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
    rd_data = DataManager.custom_encoder(user)
    for key, value in rd_data.items():
        value.pop('role')
        value.pop('password')
    data_dict = dict()
    data_dict.update(rd_data)
    return jsonify(data_dict), 201


@auth_bp.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    session = get_session()
    user = session.query(User).filter(User.email == email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200
