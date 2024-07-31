"""Module for places endpoint"""
from services.DataManipulation.datamanager import DataManager
from services.DataManipulation.crud import Crud
from services.Database.database import get_session
from model.place import Place
from model.place_amenity import PlaceAmenity
from model.review import Review
from flask import Blueprint, jsonify, request
from uuid import uuid4

places_bp = Blueprint('places', __name__)


@places_bp.get('/')
def get_places():
    raw_data = Crud.get('Place')
    data_dict = dict()
    for data in raw_data:
        rd_data = DataManager.custom_encoder(data)
        amenities = []
        session = get_session()
        plc_amnt = session.query(PlaceAmenity).filter(PlaceAmenity.place_id == data.id).all()
        for amenity in plc_amnt:
            amenities.append(amenity.amenity_id)
        rd_data[data.id]['amenities'] = amenities
        data_dict.update(rd_data)
    if not data_dict:
        return jsonify({'message': 'No places found'}), 200
    return jsonify(data_dict), 200


@places_bp.get('/<place_id>')
def get_place_by_id(place_id):
    raw_data = Crud.get('Place', place_id)
    if not raw_data:
        return jsonify({'error': 'Place not found'}), 404
    rd_data = DataManager.custom_encoder(raw_data)
    amenities = []
    session = get_session()
    plc_amnt = session.query(PlaceAmenity).filter(PlaceAmenity.place_id == place_id).all()
    for amenity in plc_amnt:
        amenities.append(amenity.amenity_id)
    rd_data[place_id]['amenities'] = amenities
    data_dict = dict()
    data_dict.update(rd_data)
    return jsonify(data_dict), 200


@places_bp.post('/')
def create_place():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    name = data.get('name')
    description = data.get('description')
    address = data.get('address')
    city = data.get('city')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    host = data.get('host')
    num_of_rooms = data.get('num_of_rooms')
    bathrooms = data.get('bathrooms')
    price = data.get('price')
    max_guests = data.get('max_guests')
    if (not name or not address or not city or not latitude or not longitude or not host or
            not num_of_rooms or not bathrooms or not price or not max_guests):
        return jsonify({'error': 'Missing data'}), 400
    try:
        new_place_id = str(uuid4())
        place = Place(id=new_place_id, name=name, description=description, address=address, city=city,
                      latitude=latitude, longitude=longitude, host=host, num_of_rooms=num_of_rooms,
                      bathrooms=bathrooms, price=price, max_guests=max_guests)
        DataManager.save_to_db(place)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    place = Crud.get('Place', new_place_id)
    return jsonify(DataManager.custom_encoder(place)), 201


@places_bp.put('/<place_id>')
def update_place(place_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('Place', place_id)
    if data is None:
        return jsonify({'error': 'Place not found'}), 404
    fields_to_update = ['host', 'name', 'description', 'address', 'city', 'latitude', 'longitude',
                        'num_of_rooms', 'bathrooms', 'price', 'max_guests']
    for field in fields_to_update:
        if datatoupdate.get(field):
            try:
                status = Crud.update('Place', place_id, field, datatoupdate[field])
                if status == 404:
                    return jsonify({'error': 'Place not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'Place updated'}), 201


@places_bp.delete('/<place_id>')
def delete_place(place_id):
    if not place_id:
        return jsonify({'error': 'Missing data'}), 404
    status = Crud.delete('Place', place_id)
    if status == 404:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify({'message': 'Place deleted'}), 204


@places_bp.get('/<place_id>/reviews')
def get_reviews(place_id):
    if not place_id:
        return jsonify({'error': 'Missing data'}), 400
    session = get_session()
    try:
        reviews = session.query(Review).filter(Review.place == place_id).all()
        data_dict = dict()
        for data in reviews:
            rd_data = DataManager.custom_encoder(data)
            data_dict.update(rd_data)
        if not data_dict:
            return jsonify({'message': 'No places found'}), 404
        return jsonify(data_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 200
    finally:
        session.close()


@places_bp.post('/<place_id>/reviews')
def add_reviews(place_id):
    if not place_id:
        return jsonify({'error': 'Missing data'}), 400
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    feedback = data.get('feedback')
    rating = data.get('rating')
    user = data.get('user')
    if not rating or not user:
        return jsonify({'error': 'Missing data'}), 400
    try:
        new_review_id = str(uuid4())
        review = Review(id=new_review_id, user=user, place=place_id, feedback=feedback, rating=rating)
        DataManager.save_to_db(review)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    review = Crud.get('Review', new_review_id)
    return jsonify(DataManager.custom_encoder(review)), 201
