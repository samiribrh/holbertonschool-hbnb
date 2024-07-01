"""Module for places endpoint"""
from Services.DataManipulation.crud import Crud
from Services.Validators.validators import Validator
from env.env import datafile
from Model.place import Place
from Model.review import Review
from flask import Blueprint, jsonify, request
import json

places_bp = Blueprint('places', __name__)


@places_bp.route('/', methods=['GET'])
def get_places():
    data = Crud.get('Place')
    return jsonify(data), 200


@places_bp.route('/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    data = Crud.get('Place', place_id)
    if data is None:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(data), 200


@places_bp.route('/', methods=['POST'])
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
    amenities = data.get('amenities')
    if (not name or not description or not address or not city or not latitude or not longitude or not host or
            not num_of_rooms or not bathrooms or not price or not max_guests):
        return jsonify({'error': 'Missing data'}), 400
    try:
        place = Place(name, description, address, city, latitude, longitude, host, num_of_rooms,
                      bathrooms, price, max_guests, amenities)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(place.__dict__), 201


@places_bp.route('/<place_id>', methods=['PUT'])
def update_place(place_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('Place', place_id)
    if data is None:
        return jsonify({'error': 'Place not found'}), 404
    if not Validator.validate_city(datatoupdate.get('city')):
        return jsonify({'error': 'Invalid city'}), 400
    if not Validator.validate_coordinates(datatoupdate.get('latitude'), datatoupdate.get('longitude')):
        return jsonify({'error': 'Invalid coordinates'}), 400
    if not (Validator.is_positive_int(datatoupdate.get('num_of_rooms')),
            Validator.is_positive_int(datatoupdate.get('bathrooms')),
            Validator.is_positive_int(datatoupdate.get('max_guest')),):
        return jsonify({'error': 'num_of_rooms, bathrooms, max_guests should be positive integers'}), 400
    price = datatoupdate.get('price')
    if not ((isinstance(price, int) or isinstance(price, float)) and (price >= 0)):
        return jsonify({'error': 'Invalid price'}), 400
    for amenity in datatoupdate.get('amenities'):
        if not Validator.check_valid_amenity(amenity):
            return jsonify({'error': 'Invalid amenity'}), 400
    data['name'] = datatoupdate.get('name')
    data['description'] = datatoupdate.get('description')
    data['address'] = datatoupdate.get('address')
    data['city'] = datatoupdate.get('city')
    data['latitude'] = datatoupdate.get('latitude')
    data['longitude'] = datatoupdate.get('longitude')
    data['num_of_rooms'] = datatoupdate.get('num_of_rooms')
    data['bathrooms'] = datatoupdate.get('bathrooms')
    data['price'] = datatoupdate.get('price')
    data['max_guests'] = datatoupdate.get('max_guests')
    data['amenities'] = datatoupdate.get('amenities')
    if (not data['name'] or not data['description'] or not data['address'] or not data['city'] or
            not data['latitude'] or not data['longitude'] or not data['num_of_rooms'] or
            not data['bathrooms'] or not data['price'] or not data['max_guests']):
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.update(place_id, 'Place', data)
    if status == 404:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify({'message': 'Place updated'}), 200


@places_bp.route('/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    if not place_id:
        return jsonify({'error': 'Missing data'}), 404
    status = Crud.delete(place_id, 'Place')
    if status == 404:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify({'message': 'Place deleted'}), 204


@places_bp.route('/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    if not place_id:
        return jsonify({'error': 'Missing data'}), 400
    plcdata = Crud.get('Place', place_id)
    plcreviews = plcdata.get('reviews')
    if not plcreviews:
        return jsonify({'message': 'No review found'}), 200
    with open(datafile, 'r') as file:
        data = json.loads(file.read())
    reviews = data['Review']
    reviewstoreturn = dict()
    for review in plcreviews:
        reviewstoreturn[review] = reviews.get(review)
    return jsonify(reviewstoreturn), 200


@places_bp.route('/<place_id>/reviews', methods=['POST'])
def add_reviews(place_id):
    if not place_id:
        return jsonify({'error': 'Missing data'}), 400
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    feedback = data.get('feedback')
    rating = data.get('rating')
    user = data.get('user')
    try:
        review = Review(feedback, rating, user, place_id)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
