"""this will allow us to use the auth blueprint"""
from . import auth_blueprint

"""allow us to test the user model"""
from app.models import User

"""this will allow us to make responses from requests and jsonify to encode response"""
from flask import make_response, request,jsonify

"""allow us to create view functions"""
from flask.views import MethodView


class RegistrationView(MethodView):
    """this class will handle registration of users"""

    def post(self):
        """this method will handle post requests 
        It will handle registering users to the database"""

        """first check if the email exists"""
        user=User.query.filter_by(email=request.data['email']).first()

        if not user:
            """if the user does not exist"""
            try:
                post_data=request.data

                #get the data from the request
                email=post_data['email']
                password=post_data['password']
                confirm_password=post_data['confirm_password']
                #validate email
                valid_email=User.validate_email(email)
                valid_password_length=User.validate_password_length(password)
                valid_password_format=User.validate_password_format(password)

                if password == confirm_password and valid_email and valid_password_length and valid_password_format:
                    user=User(email=email,password=password)
                    user.save()

                    response={
                        "message":"successfully registered user"
                    }
                    #return response to notify user that they have been registered
                    #make_response() is used for returning responses

                    return make_response(jsonify(response)),201

                elif password != confirm_password:
                    response={
                        "message":"password and confirm_password have to match"
                    }
                    return make_response(jsonify(response)),400

                elif not valid_email:
                    response={
                        "message":"enter valid email"
                    }
                    return make_response(jsonify(response)),400

                elif not valid_password_length:
                    response={
                        "message":"password length should be greater than 6"
                    }
                    return make_response(jsonify(response)),400

                else:
                    response={
                        "message":"email cannot be empty"
                    }
                    return make_response(jsonify(response)),400



            except Exception as e:
                response={
                    "message":str(e)
                }
                print(response)
                return make_response(jsonify(response)),401

        else:
            """this will run if the user exists"""
            response={
                "message":"user already exists"
            }

            return make_response(jsonify(response)),409


class LoginView(MethodView):
    """this is the class to login the user"""
    def post(self):
        """the method to handle post request to the login route"""
        try:
            """get the user who matches the email entered"""
            user=User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                """generate access token"""
                access_token=user.generate_token(user.id)
                if access_token:
                    response={
                        "message":"you logged in successfully",
                        "access_token":access_token.decode()
                    }

                    return make_response(jsonify(response)),200

            else:
                """if user does not exist"""
                response={
                    "message":"invalid email or password"
                }
                return make_response(jsonify(response)),401        
                

        except Exception as e:

            response={
                "message":str(e)
            }
            print(str(e))
            return make_response(jsonify(response)),500



"""MAKE THE CLASS CALLABLE SO THAT IT
CAN TAKE REQUESTS AND RETURN RESPONSES"""

registration_view=RegistrationView.as_view('registration_view')
login_view=LoginView.as_view('login_view')

"""add url rule to the blueprint"""
"""pass in the url, view and method"""
auth_blueprint.add_url_rule('/api/v2/auth/registration',view_func=registration_view,methods=['POST'])
auth_blueprint.add_url_rule('/api/v2/auth/login',view_func=login_view,methods=['POST'])            