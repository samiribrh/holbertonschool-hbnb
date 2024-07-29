"""Module for reviews endpoint"""
from services.DataManipulation.datamanager import DataManager
from services.DataManipulation.crud import Crud
from flask import Blueprint, jsonify, request

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.get('/<review_id>')
def get_review_by_id(review_id):
    raw_data = Crud.get('Review', review_id)
    if not raw_data:
        return jsonify({'error': 'Review not found'}), 404
    rd_data = DataManager.custom_encoder(raw_data)
    data_dict = dict()
    data_dict.update(rd_data)
    return jsonify(data_dict), 200


@reviews_bp.put('/<review_id>')
def update_review(review_id):
    datatoupdate = request.get_json()
    if not datatoupdate:
        return jsonify({'error': 'No data'}), 400
    data = Crud.get('Review', review_id)
    if data is None:
        return jsonify({'error': 'Review does not exist'}), 404
    fields_to_update = ['rating', 'feedback']
    for field in fields_to_update:
        if datatoupdate.get(field):
            try:
                status = Crud.update('Review', review_id, field, datatoupdate[field])
                if status == 404:
                    return jsonify({'error': 'Place not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'Review updated'}), 200


@reviews_bp.delete('/<review_id>')
def delete_review(review_id):
    if not review_id:
        return jsonify({'error': 'Missing data'}), 400
    status = Crud.delete('Review', review_id)
    if status == 404:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify({'message': 'Review deleted'}), 204
