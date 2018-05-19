from flask import Blueprint
#initialize the blueprint
auth_blueprint=Blueprint('auth', __name__)
from . import views