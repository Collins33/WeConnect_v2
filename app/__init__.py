from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

#import the environment dict
from instance.config import app_config

from flask import request, jsonify, abort,session

#initialize sqlalchemy
db=SQLAlchemy()

def create_app(config_name):
    from app.models import Business, User
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
        #get access token from the header
        auth_header=request.headers.get('Authorization')
        access_token=auth_header.split(" ")[1]

        if access_token:
            """user is legit"""
            #decode the access_token and get the user_id
            user_id=User.decode_token(access_token)

            #get the user data
            name = str(request.data.get('name', ''))          
            description=str(request.data.get('description', ''))
            location=str(request.data.get('location', ''))
            contact=str(request.data.get('contact', ''))
            category=str(request.data.get('category',''))

            #ensure all the data is there
            if name and description and location and contact and category:
                business=Business(name=name,description=description,location=location,contact=contact,category=category,business_owner=user_id)
                business.save()

                creation_response=jsonify({
                    'id':business.id,
                    'name':business.name,
                    'description':business.description,
                    'location':business.location,
                    'contact':business.contact,
                    'category':business.category,
                    'business_owner':business.business_owner
                })

                creation_response.status_code=201
                return creation_response
                

            else:
                message="Enter all the details"
                #400 is bad request
                response=jsonify({'message':message,'status':400})
                response.status_code=400
                return response

        # else:
        #     """user is not legit"""
        #     message = user_id
        #     response = {
        #             'message': message
        #         }
        #     return make_response(jsonify(response)), 401



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

    @app.route('/api/v2/businesses/<int:id>', methods=['GET'])
    def get_single_business(id):
        business=Business.query.filter_by(id=id).first()
        if not business:
            #check if the business exists
            message="business does not exist"
            response=jsonify({"message":message,"status_code":404})
            #404 if business does not exist
            response.status_code=404
            return response

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

    @app.route('/api/v2/businesses/<int:id>', methods=['PUT'])
    def edit_business(id):
        business=Business.query.filter_by(id=id).first()
        if not business:
            #check if the business exists
            message="business does not exist"
            response=jsonify({"message":message,"status_code":404})
            #404 if business does not exist
            response.status_code=404
            return response

        #get access token from the header
        auth_header=request.headers.get('Authorization')
        access_token=auth_header.split(" ")[1]

        if access_token:
            #if access token exists, user can edit business
            #get data from the requested data
            business_owner=User.decode_token(access_token)

            
            name = str(request.data.get('name', ''))          
            description=str(request.data.get('description', ''))
            location=str(request.data.get('location', ''))
            contact=str(request.data.get('contact', ''))
            category=str(request.data.get('category',''))
            
            #replace the details of the found business
            business.name=name,
            business.description=description,
            business.location=location,
            business.contact=contact,
            business.category=category
            #save the business
            business.save()

            response=jsonify({

                'id':business.id,
                'name':business.name,
                'description':business.description,
                'location':business.location,
                'contact':business.contact,
                'category':business.category,
                'business_owner':business.business_owner
            })

            response.status_code=200
            return response

    @app.route('/api/v2/businesses/<int:id>', methods=['DELETE'])
    def delete_business(id):
        business=Business.query.filter_by(id=id).first()

        if not business:
            #check if the business exists
            message="business does not exist"
            response=jsonify({"message":message,"status_code":404})
            #404 if business does not exist
            response.status_code=404
            return response


        #get access token from the header
        auth_header=request.headers.get('Authorization')
        access_token=auth_header.split(" ")[1]

        if access_token:
            #if access_token exists, delete business
            business.delete_business()
            response=jsonify({"message":"business successfully deleted","status_code":200})
            response.status_code=200
            return response    






    return app