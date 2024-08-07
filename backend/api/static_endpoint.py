from core.config import Config
from flask import Blueprint, send_from_directory

static_bp = Blueprint('static', __name__)


@static_bp.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(Config.STATIC_FOLDER, filename)

