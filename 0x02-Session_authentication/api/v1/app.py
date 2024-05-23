#!/usr/bin/env python3
"""
Route module for the API
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from logging import FileHandler, WARNING
import os


app = Flask(__name__)
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

my_auth = os.environ.get('AUTH_TYPE')
if my_auth == 'basic_auth':
    auth = BasicAuth()
if my_auth == 'session_auth':
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def before_request() -> str:
    """ Before request handler"""
    if auth is None:
        return
    notsubset_path = ['/api/v1/status/',
                      '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if auth.require_auth(request.path, notsubset_path) is False:
        return
    if auth.authorization_header(request) is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
