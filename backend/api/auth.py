"""Authorization Endpoints"""
from uuid import uuid4

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash

from model.user import User

from services.Database.database import get_session
from services.DataManipulation.crud import Crud
from services.DataManipulation.datamanager import DataManager
from services.Tasks.email_service import send_verification

from utils.otp_generator import generate_otp

from core.redis_config import redis_cli
from core.config import Config


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
    if not (email and password and first_name and last_name):
        return jsonify({'error': 'Missing data'}), 400
    try:
        new_user_id = str(uuid4())
        new_user = User(id=new_user_id, email=email, password=password,
                        first_name=first_name, last_name=last_name)
        DataManager.save_to_db(new_user)

        verification_code = generate_otp()
        redis_cli.set(f'verification_code_{email}', verification_code, ex=Config.VERIFICATION_EXPIRATION)
        send_verification(email, verification_code)
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


@auth_bp.post('/verify')
def verify():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    email = data.get('email')
    code = data.get('code')

    if not (email and code):
        return jsonify({'error': 'Missing data'}), 400

    try:
        verification_code = redis_cli.get(f'verification_code_{email}')
        if not verification_code:
            return jsonify({'error': 'Verification code expired or not found'}), 400

        if code != verification_code:
            return jsonify({'error': 'Invalid verification code'}), 400

        session = get_session()
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.is_verified = True
        session.commit()

        redis_cli.delete(f'verification_code_{email}')

        session.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'User verified'}), 200


@auth_bp.post('/resend')
def resend_verification():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Missing data'}), 400
    verification_code = redis_cli.get(f'verification_code_{email}')
    if verification_code:
        redis_cli.delete(f'verification_code_{email}')
    try:
        verification_code = generate_otp()
        redis_cli.set(f'verification_code_{email}', verification_code, ex=Config.VERIFICATION_EXPIRATION)
        send_verification(email, verification_code)
        return jsonify({"message": "Verification code sent"})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    session = get_session()
    user = session.query(User).filter(User.email == email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    if not user.is_verified:
        return jsonify({'error': 'User is not verified'}), 401

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200
