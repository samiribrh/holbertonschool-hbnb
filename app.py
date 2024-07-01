"""Module containing main app for HBnB project"""
from Services.Initializer.define_blueprints import define_blueprints
from Services.Initializer.initializer import initialize_file
from flask import Flask
import json

app = Flask(__name__)
app = define_blueprints(app)

if __name__ == '__main__':
    @app.route('/', methods=['GET'])
    def index():
        return "Hi!"

    app.run(port=5000, debug=True)

    initialize_file()
    with open('Data/datacopy.json', 'r') as file:
        data = json.loads(file.read())
    with open('Data/data.json', 'w') as file:
        file.write(json.dumps(data, indent=4))
