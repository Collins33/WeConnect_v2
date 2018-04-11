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
                user=User(email=email,password=password)
                user.save()

                response={
                    "message":"successfully registered user"
                }
                #return response to notify user that they have been registered
                #make_response() is used for returning responses

                return make_response(jsonify(response)),201

            except Exception as e:
                response={
                    "message":str(e)
                }

                return make_response(jsonify(response)),401

        else:
            """this will run if the user exists"""
            response={
                "message":"user already exists"
            }

            return make_response(jsonify(response)),202


"""MAKE THE CLASS CALLABLE SO THAT IT
CAN TAKE REQUESTS AND RETURN RESPONSES"""

registration_view=RegistrationView.as_view('registration_view')

"""add url rule to the blueprint"""
"""pass in the url, view and method"""
auth_blueprint.add_url_rule('api/v2/auth/registration',view_func=registration_view,methods=['POST'])            