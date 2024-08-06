from flask import Blueprint, send_from_directory

static_bp = Blueprint('static', __name__)


@static_bp.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(static_bp.static_folder, filename)
