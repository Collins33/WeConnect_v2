from flask import Blueprint

#create instance of blueprint
review_blueprint=Blueprint("reviews",__name__)

from . import views