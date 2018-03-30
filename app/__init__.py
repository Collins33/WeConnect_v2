from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

#import the environment dict
from instance.config import app_config

#initialize sqlalchemy
db=SQLAlchemy()

def create_app(config_name):
    """this method wraps creation of flask-api
    object and returns it after loading the configurations"""

    app=FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #connect the db
    db.init_app(app)

    return app