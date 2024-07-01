"""Module to keep custom exceptions."""


class InvalidCountryError(Exception):
    """Exception raised for invalid country value."""
    pass


class CityAlreadyExistsError(Exception):
    """Exception raised when a city already exists in the specified country."""
    pass


class AmenityAlreadyExistsError(Exception):
    """Exception raised when an amenity already exists."""
    pass


class HostNotFound(Exception):
    """Exception raised when a host is not found."""
    pass


class CityNotFound(Exception):
    """Exception raised when a city is not found."""
    pass


class PlaceAlreadyExistsError(Exception):
    """Exception raised when a place already exists."""
    pass


class AmenityNotFound(Exception):
    """Exception raised when an amenity is not found."""
    pass


class ValidNumberError(Exception):
    """Exception raised when a number is not valid."""
    pass
