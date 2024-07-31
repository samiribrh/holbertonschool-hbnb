"""Module containing main app for HBnB project"""
from services.Initializer.initializer import initialize_services
from services.Initializer.create_app import create_app
from flask import send_from_directory

app = create_app()


def main():
    initialize_services()

    @app.get('/')
    def index():
        return "Hi!"

    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)

    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    main()
