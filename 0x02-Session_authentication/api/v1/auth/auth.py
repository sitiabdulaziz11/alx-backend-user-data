#!/usr/bin/env python3
""" Auth class """

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user"""
        return None

    def session_cookie(self, request=None):
        """ Session cookie"""
        if request is None:
            return None
        session_name = os.environ.get('SESSION_NAME')
        return request.cookies.get(session_name)
