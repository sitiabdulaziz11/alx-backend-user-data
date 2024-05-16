#!/usr/bin/env python3
""" Encrypting passwords"""


import bcrypt


def hash_password(password: str) -> bytes:
    """ function that returns a salted, hashed password, which
    is a byte string"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(password: str, hashed_password: bytes) -> bool:
    """ function that returns True if the password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
