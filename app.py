"""Module containing main app for HBnB project"""
from Services.DataManipulation.crud import Crud

if __name__ == '__main__':
    from Services.Initializer.initializer import initialize_file
    import json

    initialize_file()
    with open('Data/datacopy.json', 'r') as file:
        data = json.loads(file.read())
    with open('Data/data.json', 'w') as file:
        file.write(json.dumps(data, indent=4))

    Crud.delete("a2210d09-0bec-497c-9913-ac436f2811ff", "Amenity")
