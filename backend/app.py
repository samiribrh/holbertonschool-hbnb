"""Module containing main app for HBnB project"""
from Services.Initializer.initializer import initialize_services
from Services.Initializer.create_app import create_app
from flask import redirect, url_for

app = create_app()


def main():
    initialize_services()

    @app.route('/', methods=['GET'])
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET'])
    def login():
        return "Hi!"

    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()
