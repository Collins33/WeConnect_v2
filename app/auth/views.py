from . import auth_blueprint
from app.models import User, Access_token
from flask import make_response, request, jsonify
from flask.views import MethodView


class RegistrationView(MethodView):
    """this class will handle registration of users"""
    def post(self):
        """this method will handle post requests 
        It will handle registering users to the database"""
        # first check if the email exists
        user = User.query.filter_by(email=request.data['email']).first()
        if not user:
            # if the user does not exist
            try:
                post_data = request.data
                # get the data from the request
                email = post_data['email']
                password = post_data['password']
                confirm_password = post_data['confirm_password']
                # validate email
                valid_email = User.validate_email(email)
                valid_password_length = User.validate_password_length(password)
                valid_password_format = User.validate_password_format(password)
                if password == confirm_password and valid_email and valid_password_length and valid_password_format:
                    user = User(email=email, password=password)
                    user.save()
                    register_user = []
                    response = {
                        "message": "successfully registered user"
                    }
                    register_user.append(response)

                    # return response to notify user that they have been registered
                    # make_response() is used for returning responses
                    return make_response(jsonify(register_user)), 201
                elif password != confirm_password:
                    register_user = []
                    response = {
                        "message": "password and confirm_password have to match"
                    }
                    register_user.append(response)
                    return make_response(jsonify(register_user)), 400
                elif not valid_email:
                    register_user = []
                    response = {
                        "message": "enter valid email"
                    }
                    register_user.append(response)
                    return make_response(jsonify(register_user)), 400
                elif not valid_password_length:
                    register_user = []
                    response = {
                        "message": "password length should be greater than 6"
                    }
                    register_user.append(response)
                    return make_response(jsonify(register_user)), 400
                else:
                    register_user = []
                    response = {
                        "message": "email cannot be empty"
                    }
                    register_user.append(response)
                    return make_response(jsonify(response)), 400
            except Exception as e:
                response = {
                    "message": str(e) + " is missing"
                }
                print(response)
                return make_response(jsonify(response)), 403
        else:
            # this will run if the user exists
            response = {
                "message": "user already exists"
            }
            return make_response(jsonify(response)), 409


class LoginView(MethodView):
    """this is the class to login the user"""
    def post(self):
        """the method to handle post request to the login route"""
        try:
            # get the user who matches the email entered
            user = User.query.filter_by(email=request.data['email']).first()
            if user and user.password_is_valid(request.data['password']):
                # generate access token
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        "message": "you logged in successfully",
                        "access_token": access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # if user does not exist
                response = {
                    "message": "invalid email or password"
                }
                return make_response(jsonify(response)), 401        
        except Exception as e:
            response = {
                "message": str(e)
            }
            print(str(e))
            return make_response(jsonify(response)), 500


class LogoutView(MethodView):
    def post(self):
        # get access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            my_token = Access_token(token=access_token)
            my_token.save()
            message = "You have successfully logged out"
            response = jsonify({
                "message": message, "status": 200
            })
            response.status_code = 200
            return response
        else:
            message = "You are not logged in"
            response = jsonify({
                "message": message, "status": 200
            })
            response.status_code = 200
            return response


# MAKE THE CLASS CALLABLE SO THAT IT
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
# add url rule to the blueprint
# pass in the url, view and method
auth_blueprint.add_url_rule('/api/v2/auth/registration', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule('/api/v2/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/api/v2/auth/log-out', view_func=logout_view, methods=['POST'])
            