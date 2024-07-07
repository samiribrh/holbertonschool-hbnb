"""Module containing Initializers for the project"""
from Services.database import get_session
from Model.country import Country


def initialize_countries():
    """Function to initialize the countries"""
    from env.env import countryfile
    import json

    session = get_session()
    try:
        with open(countryfile, 'r') as file:
            countries_data = json.load(file)
        existing_countries = {country.id for country in session.query(Country).all()}

        for code, name in countries_data.items():
            if code not in existing_countries:
                country = Country(id=code, name=name)
                session.add(country)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()
