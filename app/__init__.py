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

    """import auth blueprint and register it"""
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

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
                'category':business.category
            }
            final_result.append(obj)

        response=jsonify(final_result)
        response.status_code=200
        return response

    @app.route('/api/v2/businesses/<int:id>', methods=['GET','DELETE','PUT'])
    def get_single_business(id):
        business=Business.query.filter_by(id=id).first()
        if not business:
            message="business does not exist"
            response=jsonify({"message":message,"status_code":404})
            response.status_code=404
            return response
        if request.method == 'GET':

            response=jsonify({
                'id':business.id,
                'name':business.name,
                'description':business.description,
                'location':business.location,
                'contact':business.contact,
                'category':business.category
            })   
            response.status_code=200
            return response         

        elif request.method == 'DELETE':
            business.delete_business()
            message="business successfully deleted"
            response=jsonify({"message":message,"status_code":200})
            response.status_code=200
            return response

        else:
            #first get data from the input
            name = str(request.data.get('name', ''))          
            description=str(request.data.get('description', ''))
            location=str(request.data.get('location', ''))
            contact=str(request.data.get('contact', ''))
            category=str(request.data.get('category',''))

            #replace values in the found business
            business.name=name
            business.description=description
            business.location=location
            business.contact=contact
            business.category=category

            #save the business
            business.save()

            #create response with the saved business
            response=jsonify({
                'id':business.id,
                'name':business.name,
                'description':business.description,
                'location':business.location,
                'contact':business.contact,
                'category':business.category
            })
            response.status_code=200
            return response



    @app.route('/api/v2/businesses/<string:location>', methods=['GET'])
    def filter_location(location):
        """get business based on location"""

        businesses=Business.get_business_location(location)
        business_location=[]

        if not businesses:
            message="No business in that location"
            response=jsonify({"message":message,"status_code":404})
            response.status_code=404
            return response
        else:
            for business in businesses:
                obj={
                    'id':business.id,
                    'name':business.name,
                    'description':business.description,
                    'location':business.location,
                    'contact':business.contact,
                    'category':business.category
                }
                business_location.append(obj)

            response=jsonify(business_location)
            response.status_code=200
            return response


    @app.route('/api/v2/businesses/<string:category>', methods=['GET'])
    def filter_category(category):
        """get business based on category"""

        businesses=Business.get_business_category(category)
        business_category=[]

        if not businesses:
            message="No business in that category"
            response=jsonify({"message":message,"status_code":404})
            response.status_code=404
            return response
        else:
            for business in businesses:
                obj={
                    'id':business.id,
                    'name':business.name,
                    'description':business.description,
                    'location':business.location,
                    'contact':business.contact,
                    'category':business.category
                }
                business_category.append(obj)

            response=jsonify(business_category)
            response.status_code=200
            return response                

                



    

    return app