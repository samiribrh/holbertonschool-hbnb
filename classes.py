"""Module containing entities or classes for HBnB project"""
from uuid import uuid4
from datetime import datetime


class Country:
    """The Country Class"""
    countries = []

    def __init__(self, name: str):
        """Initialization of Country Instance"""
        self.id = uuid4()
        self.name = name
        self.cities = []
        self.created_at = datetime.now()
        Country.countries.append(self)

    @staticmethod
    def validate_country(country: str):
        """Method to validate country"""
        for countryinctr in Country.countries:
            if countryinctr.name == country:
                return countryinctr
        return None

    def validate_city(self, city: str):
        """Method to validate city"""
        for ct in self.cities:
            if ct.name == city:
                return ct
        return None


class City:
    """The City Class"""
    def __init__(self, name: str, country: str):
        """Initialization of City Instance"""
        country = Country.validate_country(country)
        if country is not None:
            self.id = uuid4()
            self.name = name
            self.country = country
            self.created_at = datetime.now()
            self.places = []
            country.cities.append(self)
        else:
            raise ValueError(f"Country '{country}' not found. Cannot create city.")


class User:
    """The User Class"""
    def __init__(self, email: str, password: str, first_name: str, last_name: str):
        """Initializing an instance"""
        self.id = uuid4()
        self.email = email
        self.__password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.now()
        self.host_places = []
        self.reviews = []

    def add_place(self, name: str, description: str, address: str, country: str, city: str, latitude: float,
                  longtitude: float, num_of_rooms: int, bathrooms: int, price: float, max_guest: int, amenities=None):
        """Method to create a new Place"""
        new = Place(self, name, description, address, country, city, latitude, longtitude, num_of_rooms, bathrooms,
                    price, max_guest, amenities)
        self.host_places.append(new)
        return new

    def add_amenity(self, name: str, place: str):
        """Method to add a new amenity to a place"""
        found = 0
        for plc in self.host_places:
            if plc.name == place:
                found = 1
                place = plc
                break
        if not found:
            raise ValueError(f"Place '{place}' is not a hosted place.")
        amenity = Amenity.validate_amenity(name)
        if amenity not in place._amenities:
            place._amenities.append(amenity)
        else:
            raise ValueError(f"Amenity '{amenity.name}' already in Place '{Place}")


class Amenity:
    """The Amenity Class"""
    amenities = []

    def __init__(self, name: str):
        """Initializing Amenity instance"""
        self.id = uuid4()
        self.name = name
        self.created_at = datetime.now()
        Amenity.amenities.append(self)

    @staticmethod
    def validate_amenity(amenity: str):
        """Method to validate Amenity"""
        for amen in Amenity.amenities:
            if amen.name == amenity:
                return amen
        validate = input(f"Amenity '{amenity}' is not been found. Do you want to create?(y/n)")
        if validate.lower() == 'y':
            amenity = Amenity(amenity)
            return amenity
        else:
            return None


class Place:
    """The Place Class"""
    places = []

    def __init__(self, host: User, name: str, description: str, address: str, country: str, city: str, latitude: float,
                 longitude: float, rooms: int, bathrooms: int, price: float, max_guest: int, amenities=None):
        """Initializing Place instance"""
        country = Country.validate_country(country)
        if country is not None:
            city = country.validate_city(city)
            if city is not None:
                self.id = uuid4()
                self.name = name
                self.host = host
                self.description = description
                self.address = address
                self.city = city
                self.country = country
                self.latitude = latitude
                self.longitude = longitude
                self.num_of_rooms = rooms
                self.bathrooms = bathrooms
                self.price_per_night = price
                self.max_guest = max_guest
                self.reviews = []
                self.amenities = amenities
                self.created_at = datetime.now()
                city.places.append(self)
            else:
                raise ValueError(f"City '{city}' not found. Place can not be added.")
        else:
            raise ValueError(f"Country '{country}' not found. Place can not be added.")

    @property
    def amenities(self):
        """Getter for amenities attribute"""
        return self._amenities

    @amenities.setter
    def amenities(self, value):
        """Setter for amenities attribute"""
        amenities = []
        if (value is not None and isinstance(value, list)
                and all(isinstance(item, str) for item in value)):
            for item in value:
                amen = Amenity.validate_amenity(item)
                if amen is not None:
                    amenities.append(amen)
            self._amenities = amenities
        else:
            self._amenities = []

    def write_review(self, user: User, feedback: str, rating: float):
        """Method to add a new review"""
        review = Review(feedback, rating, user, self)
        return review


class Review:
    """The Review Class"""
    def __init__(self, feedback: str, rating: float, user: User, place: Place):
        """Initializing a new review instance"""
        if place in user.host_places:
            raise ValueError("User cannot write review for their own place.")
        self.id = uuid4()
        self.feedback = feedback
        self.rating = rating
        self.user = user
        self.place = place
        self.created_at = datetime.now()
        place.reviews.append(self)
        user.reviews.append(self)
