from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
# import the environment dict
from instance.config import app_config
from flask import request, jsonify
from flask_mail import Mail, Message
import os
import random
from flask_cors import CORS
# initialize sqlalchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Business, User, Review, Access_token
    # this method wraps creation of flask-api object and returns it after loading the configurations
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connect the db
    db.init_app(app)
    CORS(app)
    mail = Mail(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = os.environ['PORT']
    app.config['MAIL_USERNAME'] = os.environ['MAIL']
    app.config['MAIL_PASSWORD'] = os.environ['PASSWORD']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    # import auth blueprint and register it
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.route('/', methods=['GET'])
    def welcome():
        message = "Welcome to WeConnect"
        response = jsonify({'message': message, 'status': 200})
        response.status_code = 200
        return response

    @app.errorhandler(404)
    def error(e):
        message = "That page does not exist"
        response = jsonify({'message': message, 'status': 404})
        response.status_code = 404
        return response

    @app.route('/api/v2/auth/reset-password', methods=['POST'])
    def reset_password():
        # get email from the request
        email = str(request.data.get('email', ''))
        # get the user who matches the email
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            message = "Password successfully reset.Check email for new password"
            response = jsonify({"message": message, "status": 200})
            response.status_code = 200
            print(response)
            try:
                return response
            finally:

                # if the user with the email actually exists
                # generate a random string
                number = random.randint(1000, 2000) 
                password = "kiblymonkey"+str(number)
                # update details
                print(password)
                User.update(User, user.id, password=password)
                msg = Message('Hello', sender='collinsnjau39@gmail.com', recipients=[email])
                msg.body = "Your new password is {}".format(str(password))
                mail.send(msg)
        message = "Email does not exist"
        response = jsonify({"message": message, "status": 400})
        response.status_code = 400
        return response

    @app.route('/api/v2/admin/users', methods=['GET'])
    def get_users():
        """this will return a list of all user emails"""
        users = User.get_all_users()
        final_result = []
        for user in users:
            obj = {
                'email': user.email
            }
            final_result.append(obj)
        response = jsonify(final_result)
        response.status_code = 200
        return response    
      
    # BUSINESS ENDPOINTS
    @app.route('/api/v2/businesses', methods=['POST'])
    def add_business():
        # get access token from the header
        auth_header = request.headers.get('Authorization')
        if auth_header:

            access_token = auth_header.split(" ")[1]
            # return true if token is valid
            valid_token = Access_token.query.filter_by(token=access_token).first() 
            if not valid_token:
                # user is legit
                # decode the access_token and get the user_id
                user_id = User.decode_token(access_token)
                # get the user data
                name = str(request.data.get('name', ''))          
                description = str(request.data.get('description', ''))
                location = str(request.data.get('location', ''))
                contact = str(request.data.get('contact', ''))
                category = str(request.data.get('category', ''))
                # validate user data
                validate_name = Business.validate_business_details(name)
                business_exist = Business.query.filter_by(name=name).first()
                if not business_exist:
                    if name and description and location and contact and category:
                        if validate_name:
                            business = Business(name=name, description=description, location=location, contact=contact, category=category, business_owner=user_id)
                            business.save()
                            creation_response = jsonify({
                                'id': business.id,
                                'name': business.name,
                                'description': business.description,
                                'location': business.location,
                                'contact': business.contact,
                                'category': business.category,
                                'business_owner': business.business_owner
                            })
                            creation_response.status_code = 201
                            return creation_response
                        else:
                            message = "details cannot be empty string"
                            # 400 is bad request
                            response = jsonify({'message': message, 'status': 400})
                            response.status_code = 400
                            return response
                    elif not description:
                        message = "Business description missing"
                        response = jsonify({'message': message, 'status': 400})
                        response.status_code = 400
                        return response
                    elif not location:
                        message = "Business location missing"
                        response = jsonify({'message': message, 'status': 400})
                        response.status_code = 400
                        return response
                    elif not contact:
                        message = "Business contact missing"
                        response = jsonify({'message': message, 'status': 400})
                        response.status_code = 400
                        return response
                    else:
                        message = "Business category missing"
                        response = jsonify({'message': message, 'status': 400})
                        response.status_code = 400
                        return response
                else:
                    # if business name exists
                    message = "Business name already exists"
                    response = jsonify({
                        "message": message, 'status': 409
                    })
                    response.status_code = 409
                    return response
            else:
                # user is not legit
                message = "You are not logged in. Please log in"
                response = jsonify({
                    "message": message
                })
                response.status_code = 403
                return response
        message = "You must have a token to add a business. Login to get a token"
        response = jsonify({"message": message, "status": 403})
        response.status_code = 403
        return response

    @app.route('/api/v2/dashboard', methods=['GET'])
    def dashboard():
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
            # return true if token is valid
            valid_token = Access_token.query.filter_by(token=access_token).first()
            if not valid_token:
                # this user is legit and authorized get the id
                user_id = User.decode_token(access_token)
                # use the user id to get businesses owned by the user
                businesses = Business.get(user_id)
                final_result = []
                for business in businesses:
                    obj = {
                        'id': business.id,
                        'name': business.name,
                        'description': business.description,
                        'location': business.location,
                        'contact': business.contact,
                        'category': business.category
                    }
                    final_result.append(obj)
                response = jsonify(final_result)
                response.status_code = 200
                return response
        message = "You must be logged in to access the dashboard"
        response = jsonify({"message": message, "status": 403})
        response.status_code = 403
        return response
 
    @app.route('/api/v2/businesses', methods=['GET'])
    def all_business():
        """this will get all the businesses"""
        businesses = Business.get_all()
        final_result = []
        for business in businesses:
            obj = {
                'id': business.id,
                'name': business.name,
                'description': business.description,
                'location': business.location,
                'contact': business.contact,
                'category': business.category
            }
            final_result.append(obj)
        response = jsonify(final_result)
        response.status_code = 200
        return response
    
    @app.route('/api/v2/business/paginate/page=<int:page>&limit=<int:limit>', methods=['GET'])
    def paginate_business(limit=4, page=1):
        """get a given number of business"""
        businesses = Business.query.paginate(page, per_page=limit, error_out=True)
        final_result = []
        for business in businesses.items:
            obj = {
                'id': business.id,
                'name': business.name,
                'description': business.description,
                'location': business.location,
                'contact': business.contact,
                'category': business.category
            }
            final_result.append(obj)
        response = jsonify(final_result)
        response.status_code = 200
        return response

    @app.route('/api/v2/businesses/<int:id>', methods=['GET'])
    def get_single_business(id):
        business = Business.query.filter_by(id=id).first()
        if not business:
            # check if the business exists
            message = "business does not exist"
            response = jsonify({"message": message, "status_code": 404})
            # 404 if business does not exist
            response.status_code = 404
            return response
        final_result = []
        obj = {
            'id': business.id,
            'name': business.name,
            'description': business.description,
            'location': business.location,
            'contact': business.contact,
            'category': business.category
        }
        final_result.append(obj)
        response = jsonify(final_result)
        response.status_code = 200
        return response

    @app.route('/api/v2/businesses/<int:id>', methods=['PUT'])
    def edit_business(id):
        business = Business.query.filter_by(id=id).first()
        if not business:
            # check if the business exists
            message = "business does not exist"
            response = jsonify({"message": message, "status_code": 404})
            # 404 if business does not exist
            response.status_code = 404
            return response
        # get access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        valid_token = Access_token.query.filter_by(token=access_token).first() 
        if not valid_token:
            # if access token exists, user can edit business
            # get data from the requested data
            business_owner = User.decode_token(access_token)
            real_owner = business.business_owner
            # check if logged in id is equal to id of business owner
            if business_owner == real_owner:
                name = str(request.data.get('name', ''))          
                description = str(request.data.get('description', ''))
                location = str(request.data.get('location', ''))
                contact = str(request.data.get('contact', ''))
                category = str(request.data.get('category', ''))
                # ensure all the fields are available
                if name and description and location and contact and category:
                    # replace the details of the found business
                    business.name = name,
                    business.description = description,
                    business.location = location,
                    business.contact = contact,
                    business.category = category
                    # save the business
                    business.save()
                    response = jsonify({
                        'id': business.id,
                        'name': business.name,
                        'description': business.description,
                        'location': business.location,
                        'contact': business.contact,
                        'category': business.category,
                        'business_owner': business.business_owner
                    })
                    response.status_code = 200
                    return response
                else:
                    message = "No field can be empty when updating a business"
                    response = jsonify({
                        "message": message, "status": 400
                    })
                    response.status_code = 400
                    return response
            # response if user who did not add the business tries to edit it
            message = "You cannot update a business you did not add"
            response = jsonify({"message": message, "status_code": 401})
            response.status_code = 401
            return response
        else:
            """user is not legit"""
            message = "You are not logged in. Please log in"
            response = jsonify({
                "message": message
            })
            response.status_code = 403
            return response

    @app.route('/api/v2/businesses/<int:id>', methods=['DELETE'])
    def delete_business(id):
        business = Business.query.filter_by(id=id).first()
        if not business:
            # check if the business exists
            message = "business does not exist"
            response = jsonify({"message": message, "status_code": 404})
            # 404 if business does not exist
            response.status_code = 404
            return response
        # get access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        valid_token = Access_token.query.filter_by(token=access_token).first()
        if not valid_token:
            # if access_token exists, delete business
            business_owner = User.decode_token(access_token)
            real_owner = business.business_owner
            if business_owner == real_owner:
                business.delete_business()
                response = jsonify({"message": "business successfully deleted", "status_code": 200})
                response.status_code = 200
                return response
            # response if user who did not add the business tries to delete it
            message = "You cannot delete a business you did not add"
            response = jsonify({"message": message, "status_code": 401})
            response.status_code = 401
            return response   
        else:
            """user is not legit"""
            message = "You are not logged in. Please log in"
            response = jsonify({
                "message": message
            })
            response.status_code = 403
            return response

    @app.route('/api/v2/businesses/searches', methods=['GET'])
    def search():
        searches = request.args
        search = searches.get('q')
        operators = "%" + search + "%"
        businesses = Business.query.filter(Business.name.ilike(operators)) # list with businesses
        final_result = []
        for business in businesses:
            if business:
                obj ={
                    'id': business.id,
                    'name': business.name,
                    'description': business.description,
                    'location': business.location,
                    'contact': business.contact,
                    'category': business.category
                }
            final_result.append(obj)
            response = jsonify(final_result)
            response.status_code = 200
            return response
            else:
                message = "No business found"
                response = jsonify({"message": message, "status_code": 404})
                response.status_code = 404
                return response

    @app.route('/api/v2/businesses/<string:category>', methods=['GET'])
    def filter_category(category):
        """get business based on category"""
        businesses = Business.query.filter_by(category=category)
        business_category = []
        for business in businesses:
            obj = {
                'id': business.id,
                'name': business.name,
                'description': business.description,
                'location': business.location,
                'contact': business.contact,
                'category': business.category
            }
            business_category.append(obj)
        if not business_category:
            message = "No business in that category"
            response = jsonify({"message": message, "status_code": 404})
            response.status_code = 404
            return response
        response = jsonify(business_category)
        response.status_code = 200
        return response 

    @app.route('/api/v2/businesses/<int:id>/reviews', methods=['POST'])
    def add_review(id):
        businesses = Business.check_business_exists(id)
        all_business = []
        for business in businesses:
            obj = {
                "name": business.name
            }
            all_business.append(obj)
        if not all_business:
            message = "cannot add review business that does not exist"
            response = jsonify({"message": message, "status_code": 404})
            # 404 if business does not exist
            response.status_code = 404
            return response
        opinion = str(request.data.get('opinion', ''))
        rating = int(request.data.get('rating', ''))
        if rating and opinion:
            new_review = Review(opinion=opinion, rating=rating, business_main=id)
            new_review.save()
            message = "succesfully added the review"
            response = jsonify({"message": message})
            response.status_code = 201
            return response
        message = "make sure the opinion and rating are included"
        response = jsonify({"message": message, "status_code": 400})
        response.status_code = 400
        return response  
    
    @app.route('/api/v2/businesses/<int:id>/reviews', methods=['GET'])
    def get_reviews(id):
        businesses = Business.check_business_exists(id)
        all_business = []
        for business in businesses:
            obj = {
                "name": business.name
            }
            all_business.append(obj)
        if not all_business:
            message = "cannot get review business that does not exist"
            response = jsonify({"message": message, "status_code": 404})
            # 404 if business does not exist
            response.status_code = 404
            return response    
        reviews = Review.get_business_review(id)
        all_reviews = []
        for review in reviews:
            obj = {
                
                "opinion": review.opinion,
                "rating": review.rating
            }
            all_reviews.append(obj)
        if not all_reviews:
            message = "no reviews available"
            response = jsonify({"message": message, "status_code": 404})
            # 404 if business does not exist
            response.status_code = 404
            return response
        response = jsonify(all_reviews)
        response.status_code = 200
        return response    

    return app