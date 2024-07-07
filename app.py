"""Module containing main app for HBnB project"""
from Model.amenity import Amenity
from Model.place_amenity import PlaceAmenity
from Model.city import City
from Services.DataManipulation.datamanager import DataManager
from Model.place import Place
from Services.DataManipulation.crud import Crud
from Services.Initializer.initializer import initialize_services
from Services.Initializer.define_blueprints import define_blueprints
from Services.database import get_session
from flask import Flask

app = Flask(__name__)
app = define_blueprints(app)

session = get_session()


def main():
    initialize_services()

    @app.route('/', methods=['GET'])
    def index():
        return "Hi!"

    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()
