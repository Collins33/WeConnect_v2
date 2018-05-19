import unittest
import json
from app import create_app,db

class AuthTestCase(unittest.TestCase):
    """testcase for auth blueprint"""
    #url endpoint for authentication
    registration='/api/v2/auth/registration'
    login='/api/v2/auth/login'
    logout='/api/v2/auth/log-out'

    def setUp(self):
        self.app=create_app(config_name="testing")
        self.client=self.app.test_client
        self.user={
            'email':'collinsnjau39@gmail.com',
            'password':'colo123',
            'confirm_password':'colo123'
        }
        """connect to current context
        and connect the tables"""
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self):
        result=self.client().post(AuthTestCase.registration, data=self.user)
        return result

    def log_in(self):
        self.register_user()
        result=self.client().post(AuthTestCase.login, data=self.user)
        return result       

    def test_registration(self):
        res=self.client().post(AuthTestCase.registration, data=self.user)
        """get the response after registering"""
        result=json.loads(res.data.decode())
        #assert the results
        self.assertEqual(result['message'], 'successfully registered user')
        self.assertEqual(res.status_code,201)

    def test_registration_when_user_already_exists(self):
        """test if user can be registered twice"""
        #register the user the first time
        self.register_user()
        #register the same user the second time
        result=self.client().post(AuthTestCase.registration, data=self.user)
        response_result=json.loads(result.data.decode())
        self.assertEqual(result.status_code,409)#response shows there is conflict
        self.assertEqual(response_result['message'],"user already exists")
            
    def test_login_user(self):
        """test if the api can login a user"""
        #register the user 
        self.register_user()
        #login the user
        res=self.client().post(AuthTestCase.login, data=self.user)
        self.assertEqual(res.status_code,200)#200 means the request is successful
        result_response=json.loads(res.data.decode())
        self.assertEqual(result_response["message"],"you logged in successfully")

    def test_logout_user(self):
        """test if api can logout a user"""
        #register a user
        self.register_user()
        #login the user
        result=self.log_in()
        access_token=json.loads(result.data.decode())['access_token']
        #logout the same user
        response=self.client().post(AuthTestCase.logout,headers=dict(Authorization="Bearer "+ access_token),data={"token":access_token})
        self.assertEqual(response.status_code,200)#after successfully logging out
        self.assertIn("You have successfully logged out",str(response.data))

    def test_non_registered_user_trying_to_login(self):
        """test if non registered user can login""" 
        #try logging in the user without registering the user      
        res=self.client().post(AuthTestCase.login, data=self.user)
        self.assertEqual(res.status_code,401)#bad request 

    def test_password_and_confirm_not_match(self):
        """return the message if password is not same as confirm password"""
        user={
            'email': 'not_a_user@example.com',
            'password': 'nope',
            'confirm_password':'nope2'
        }
        #register user with the bad password match
        result=self.client().post(AuthTestCase.registration, data=user)
        self.assertEqual(result.status_code,400)#returns a bad request with appropriate message
        self.assertIn("password and confirm_password have to match", str(result.data))
        
    def test_invalid_email(self):  
        user={
            'email': 'collins.com',
            'password': 'nope22',
            'confirm_password':'nope22'
        }
        #register user with wrong email format
        result=self.client().post(AuthTestCase.registration, data=user)
        self.assertEqual(result.status_code,400)
        self.assertIn("enter valid email",str(result.data))

    def test_short_password(self):
        user={
            'email': 'collinsnjau39@gmail.com',
            'password': 'nope',
            'confirm_password':'nope'
        }
        #register user with short password
        result=self.client().post(AuthTestCase.registration, data=user)
        self.assertEqual(result.status_code,400)#bad request
        self.assertIn("password length should be greater than 6",str(result.data))

    def test_empty_password(self):
        user={
            'email': 'collinsnjau39@gmail.com',
            'password': '       ',
            'confirm_password':'       '
        }
        #register user but pass empty fields as password
        result=self.client().post(AuthTestCase.registration, data=user)
        self.assertEqual(result.status_code,400)#bad request
        self.assertIn("email cannot be empty",str(result.data))

    def tearDown(self):
        #run after every test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()            