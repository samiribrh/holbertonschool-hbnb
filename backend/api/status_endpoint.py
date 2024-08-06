"""Endpoint for status of the app"""
from flask import Blueprint, jsonify

status_bp = Blueprint('status', __name__)


@status_bp.get('/')
def status():
    return {"status": "OK"}, 200
