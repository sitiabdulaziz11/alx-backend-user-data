#!/usr/bin/env python3
""" Views for Session Authentication module"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login a user"""
    email = request.form.get('email')
    pwd = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if pwd is None or pwd == '':
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})
        user = user[0]
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Logout a user"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
