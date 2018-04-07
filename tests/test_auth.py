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
        res=self.client().post('api/v2/auth/registration', data=self.user)
        """get the response after registering"""

        result=json.loads(res.data.decode())

        #assert the results
        self.assertEqual(result['message'], 'you have successfully logged in')
        self.assertEqual(res.status_code,201)        