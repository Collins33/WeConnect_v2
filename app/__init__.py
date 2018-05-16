from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

#import the environment dict
from instance.config import app_config

from flask import request, jsonify, abort,session

#initialize sqlalchemy
db=SQLAlchemy()

def create_app(config_name):
    from app.models import Business, User, Review,Access_token
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
        valid_token=Access_token.query.filter_by(token=access_token).first() #return true if token is valid

        if not valid_token:
            """user is legit"""
            #decode the access_token and get the user_id
            user_id=User.decode_token(access_token)

            #get the user data
            name = str(request.data.get('name', ''))          
            description=str(request.data.get('description', ''))
            location=str(request.data.get('location', ''))
            contact=str(request.data.get('contact', ''))
            category=str(request.data.get('category',''))
            #validate user data
            validate_name=Business.validate_business_details(name)
            
            business_exist=Business.query.filter_by(name=name).first()

            if not business_exist:
            #first validate that the business name does not exist
                
                if name and description and location and contact and category:
                #ensure all the data is there
                    if validate_name:

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
                        message="details cannot be empty string"
                        #400 is bad request
                        response=jsonify({'message':message,'status':400})
                        response.status_code=400
                        return response
                else:
                    message="Enter all the details"
                    response=jsonify({'message':message,'status':400})
                    response.status_code=400
                    return response

            else:
                #if business name exists
                message="Business name already exists"
                response=jsonify({
                    "message":message,'status':409
                })
                response.status_code=409
                return response        

        else:
            """user is not legit"""
            message = "You are not logged in. Please log in"
            response=jsonify({
                "message":message
            })
            response.status_code=403
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
        
        valid_token=Access_token.query.filter_by(token=access_token).first() 
        if not valid_token:
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

        else:
            """user is not legit"""
            message = "You are not logged in. Please log in"
            response=jsonify({
                "message":message
            })
            response.status_code=403
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
        
        valid_token=Access_token.query.filter_by(token=access_token).first()
        if not valid_token:
            #if access_token exists, delete business
            business.delete_business()
            response=jsonify({"message":"business successfully deleted","status_code":200})
            response.status_code=200
            return response

        else:
            """user is not legit"""
            message = "You are not logged in. Please log in"
            response=jsonify({
                "message":message
            })
            response.status_code=403
            return response

    
    @app.route('/api/v2/businesses/<int:id>/reviews', methods=['POST'])
    def add_review(id):
        businesses = Business.check_business_exists(id)
        all_business=[]

        for business in businesses:
            obj={
                "name":business.name
            }
            all_business.append(obj)

        if not all_business:
            message="cannot add review business that does not exist"
            response=jsonify({"message":message,"status_code":404})
            #404 if business does not exist
            response.status_code=404
            return response


        opinion=str(request.data.get('opinion', ''))
        rating=int(request.data.get('rating', ''))

        new_review=Review(opinion=opinion,rating=rating,business_main=id)

        new_review.save()

        message="succesfully added the review"

        response=jsonify({"message":message})
        response.status_code=200
        return response
    
    @app.route('/api/v2/businesses/<int:id>/reviews', methods=['GET'])
    def get_reviews(id):
        businesses = Business.check_business_exists(id)
        all_business=[]

        for business in businesses:
            obj={
                "name":business.name
            }
            all_business.append(obj)

        if not all_business:
            message="cannot get review business that does not exist"
            response=jsonify({"message":message,"status_code":404})
            #404 if business does not exist
            response.status_code=404
            return response    

        reviews=Review.get_business_review(id)#RETURNS REVIEWS FOR THAT BUSINESS ID
        all_reviews=[]
        for review in reviews:
            obj={
                
                "opinion":review.opinion,
                "rating":review.rating
            }
            all_reviews.append(obj)
            
        if not all_reviews:
            message="no reviews available"
            response=jsonify({"message":message,"status_code":404})
            #404 if business does not exist
            response.status_code=404
            return response

        response=jsonify(all_reviews)
        response.status_code=200
        return response    




    return app