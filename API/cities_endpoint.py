"""Module for user endpoint"""
from Services.DataManipulation.crud import Crud
from Model.city import City
from flask import Blueprint, jsonify, request

cities_bp = Blueprint('cities', __name__)