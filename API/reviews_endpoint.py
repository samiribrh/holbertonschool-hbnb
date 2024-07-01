"""Module for reviews endpoint"""
from Services.DataManipulation.crud import Crud
from Model.review import Review
from flask import Blueprint, jsonify, request

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    data = Crud.get('Review', review_id)
    if data is None:
        return jsonify({'error': 'Review does not exist'}), 404
    return jsonify(data), 200


@reviews_bp.route('/<review_id>', methods=['PUT'])
def update_review(review_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('Review', review_id)
    if data is None:
        return jsonify({'error': 'Review does not exist'}), 404
    data['feedback'] = datatoupdate.get('feedback')
    data['rating'] = datatoupdate.get('rating')
    if not data['rating'] or not data['feedback']:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.update(review_id, 'Review', data)
    if status == 404:
        return jsonify({'error': 'Review does not exist'}), 404
    return jsonify({'message': 'Review updated'}), 200


@reviews_bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    if not review_id:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.delete(review_id, 'Review')
    if status == 404:
        return jsonify({'error': 'Review does not exist'}), 404
    return jsonify({'message': 'Review deleted'}), 204
