from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

#import the environment dict
from instance.config import app_config

#initialize sqlalchemy
db=SQLAlchemy()

