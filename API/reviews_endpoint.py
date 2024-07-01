"""Module for reviews endpoint"""
from Services.DataManipulation.crud import Crud
from Model.review import Review
from flask import Blueprint, jsonify, request

reviews_bp = Blueprint('reviews', __name__)

