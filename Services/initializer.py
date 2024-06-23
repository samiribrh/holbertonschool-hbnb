"""Module containing Initializers for the project"""


def initialize_file():
    """Function to initialize the data.json file"""
    from env.env import datafile, keys
    import json

    try:
        with open(datafile, 'r') as file:
            data = file.read()
            if any(data):
                data = json.loads(data)
            else:
                data = dict()
        for item in keys:
            if item not in data:
                data[item] = dict()
        with open(datafile, 'w') as file:
            file.write(json.dumps(data, indent=4))

    # If file not found, create
    except FileNotFoundError:
        with open(datafile, 'w') as file:
            data = dict()
            for item in keys:
                data[item] = dict()
            file.write(json.dumps(data, indent=4))
