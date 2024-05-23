#!/usr/bin/env python3
""" Basic Authentication class"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """ Basic Authentication class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract base64 authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
                self, base64_authorization_header: str) -> str:
        """ Decode base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':', 1)
        return credentials[0], credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ User object from credentials"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        user = User.search({'email': user_email})
        if not user:
            return None
        user_instance = user[0]
        if not user_instance.is_valid_password(user_pwd):
            return None
        return user_instance

    def test_user_object_from_credentials(
            basic_auth_instance, email, password):
        result = basic_auth_instance.user_object_from_credentials(
            email, password)
        if result:
            return "OK"  # Assuming 'OK' is the expected confirmation message
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user"""
        auth_header = self.authorization_header(request)
        base64_auth_hdr = self.extract_base64_authorization_header(auth_header)
        dec_64_authHr = self.decode_base64_authorization_header(
            base64_auth_hdr)
        user_email, user_pwd = self.extract_user_credentials(dec_64_authHr)
        return self.user_object_from_credentials(user_email, user_pwd)
