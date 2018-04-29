import unittest
import json
from app import create_app,db

class AuthTestCase(unittest.TestCase):
    """testcase for auth blueprint"""

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


    def test_registration(self):
        res=self.client().post('/api/v2/auth/registration', data=self.user)
        """get the response after registering"""

        result=json.loads(res.data.decode())

        #assert the results
        self.assertEqual(result['message'], 'successfully registered user')
        self.assertEqual(res.status_code,201)

    def test_registration_user_already_exists(self):
        """test if user can be registered twice"""
        res=self.client().post('/api/v2/auth/registration', data=self.user)
        result=self.client().post('/api/v2/auth/registration', data=self.user)

        self.assertEqual(result.status_code,409)
    
    def test_login_user(self):
        """test if the api can login a user"""
        result=self.client().post('/api/v2/auth/registration', data=self.user)
        res=self.client().post('/api/v2/auth/login', data=self.user)
        self.assertEqual(res.status_code,200)

    def test_non_registered_user(self):
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        res=self.client().post('/api/v2/auth/login', data=self.user)
        self.assertEqual(res.status_code,401)



    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()            