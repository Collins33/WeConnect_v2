"""this will allow us to use the auth blueprint"""
from . import auth_blueprint

"""allow us to test the user model"""
from app.models import User

"""this will allow us to make responses from requests and jsonify to encode response"""
from flask import make_response, request,jsonify

"""allow us to create view functions"""
from flask.views import MethodView