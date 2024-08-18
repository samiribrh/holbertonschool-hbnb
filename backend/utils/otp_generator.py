"""Module to generate OTPs"""
from random import randint


def generate_otp():
    """Generate a 6-digit OTP"""
    return randint(100000, 999999)
