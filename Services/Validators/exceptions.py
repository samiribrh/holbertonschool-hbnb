"""Module to keep custom exceptions."""


class InvalidCountryError(Exception):
    """Exception raised for invalid country value."""
    pass


class CityAlreadyExistsError(Exception):
    """Exception raised when a city already exists in the specified country."""
    pass
