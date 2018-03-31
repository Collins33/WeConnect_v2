from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

#import the environment dict
from instance.config import app_config

from flask import request, jsonify, abort,session

#initialize sqlalchemy
db=SQLAlchemy()

def create_app(config_name):
    from app.models import Business
    """this method wraps creation of flask-api
    object and returns it after loading the configurations"""

    app=FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #connect the db
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def welcome():
        message="Welcome to WeConnect"

        response=jsonify({'message':message,'status':201})
        response.status_code=201
        return response

    """BUSINESS ENDPOINTS"""
    @app.route('/api/v2/businesses',methods=['POST'])
    def add_business():
        """get business data and add business to database"""
        name = str(request.data.get('name', ''))          
        description=str(request.data.get('description', ''))
        location=str(request.data.get('location', ''))
        contact=str(request.data.get('contact', ''))
        category=str(request.data.get('category',''))

        """ensure user enters all data"""
        if name and description and location and contact and category:
            business=Business(name=name,description=description,location=location,contact=contact,category=category)

            business.save()

            response=jsonify({
                'status_code':201,
                'id':business.id,
                'name':business.name,
                'description':business.description,
                'location':business.location,
                'contact':business.contact,
                'category':business.category
            })
            

            response.status_code=201
            return response

        else:
            message="Enter all the details"
            response=jsonify({"message":message,"status_code":400})
            response.status_code=400
            return response


    @app.route('/api/v2/businesses', methods=['GET'])
    def all_business():
        """this will get all the businesses"""
        businesses=Business.get_all()

        final_result=[]
        for business in businesses:
            obj={
                'id':business.id,
                'name':business.name,
                'description':business.description,
                'location':business.location,
                'contact':business.contact,
                'caegory':business.category
            }
            final_result.append(obj)

        response=jsonify(final_result)
        response.status_code=200
        return response            
            



    return app