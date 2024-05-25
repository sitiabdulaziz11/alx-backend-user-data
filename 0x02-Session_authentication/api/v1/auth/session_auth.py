#!/usr/bin/env python3
""" Module of Session Authentication
"""

from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4
import os


class SessionAuth(Auth):
    """ Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Current user"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Destroy a Session ID"""
        if request is None:
            return False
        request_cookie = request.cookies.get(request)
        if request_cookie is None:
            return False
        user_session_id = self.user_id_for_session_id(request_cookie)
        if user_session_id is None:
            return False
        self.user_id_by_session_id.pop(user_session_id)
        return True
