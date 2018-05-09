import unittest
import json
from app import db,create_app

class ReviewsTestCase(unittest.TestCase):
    """class for testing reviews"""
    def setUp(self):
        """initilize the app and 
        set test variables"""
        self.app=create_app(config_name="testing")
        self.client=self.app.test_client
        self.review={"opinion":"Good business with good food","rating":5}
        self.business={'name':'crastycrab','description':'Fastfood','contact':'0702848032','category':'fastfood','location':'atlantic'}

        #bind app to the current context
        with self.app.app_context():
            #create db tables
            db.create_all()

    def register_user(self,email="collins.muru@andela.com",password="123test",confirm_password="123test"):
        """this method will register a user"""
        user_data={
            'email':email,
            'password':password,
            'confirm_password':confirm_password
        }
        return self.client().post('/api/v2/auth/registration',data=user_data)

    def login_user(self,email="collins.muru@andela.com",password="123test"):
        user_data={
            'email':email,
            'password':password
        }
        return self.client().post('/api/v2/auth/login',data=user_data)

    def add_business(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        response=self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        return response        

    def test_review_creation(self):
        #first add the business
        self.add_business()
        result=self.client().post('api/v2/businesses/1/reviews', data=self.review)
        self.assertEqual(result.status_code,200)

    def test_review_get_all(self):
        self.add_business()
        self.client().post('api/v2/businesses/1/reviews', data=self.review)
        result=self.client().get('api/v2/businesses/1/reviews')
        self.assertEqual(result.status_code,200)

    def test_review_not_exist(self):
        self.add_business()
        result=self.client().get('api/v2/businesses/1/reviews')
        self.assertEqual(result.status_code,404)

    def test_add_review_business_not_exist(self):
        result=self.client().post('api/v2/businesses/10/reviews', data=self.review)
        self.assertEqual(result.status_code,404)
        self.assertIn('cannot add review business that does not exist', str(result.data))

    def test_get_review_business_not_exist(self):
        self.add_business()
        self.client().post('api/v2/businesses/1/reviews', data=self.review)
        result=self.client().get('api/v2/businesses/5/reviews')
        self.assertEqual(result.status_code,404)
                  





    def tearDown(self):
        """run after every test to ensure database is empty"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()        
