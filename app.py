"""Module containing main app for HBnB project"""


if __name__ == '__main__':
    from Services.initializer import initialize_file
    import json

    initialize_file()
    with open('Data/datacopy.json', 'r') as file:
        data = json.loads(file.read())
    with open('Data/data.json', 'w') as file:
        file.write(json.dumps(data, indent=4))
