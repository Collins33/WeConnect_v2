import unittest
import json
from app import db,create_app

class ReviewsTestCase(unittest.TestCase):
    #reviews url
    review_url='api/v2/businesses/{}/reviews'
    """class for testing reviews"""
    def setUp(self):
        """initilize the app and 
        set test variables"""
        self.app=create_app(config_name="testing")
        self.client=self.app.test_client
        self.review={"opinion":"Good business with good food","rating":5}
        self.wrong_review={"rating":5}
        self.wrong_rating={"opinion":"Good business with good food"}
        self.business={'name':'crastycrab','description':'Fastfood','contact':'0702848032','category':'fastfood','location':'atlantic'}
        #bind app to the current context
        with self.app.app_context():
            #create db tables
            db.create_all()

    def register_user(self,email,password,confirm_password):
        """this method will register a user"""
        user_data={
            'email':email,
            'password':password,
            'confirm_password':confirm_password
        }
        return self.client().post('/api/v2/auth/registration',data=user_data)

    def login_user(self,email,password,confirm_password):
        user_data={
            'email':email,
            'password':password,
            'confirm_password':confirm_password
        }
        return self.client().post('/api/v2/auth/login',data=user_data)

    def add_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user("collins.muru@andela.com","123test","123test")
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        response=self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        return response        

    def test_review_creation(self):
        #first add the business
        self.add_business()
        #add the review for the business
        result=self.client().post(ReviewsTestCase.review_url.format('1'), data=self.review)
        self.assertEqual(result.status_code,201)#review created
        self.assertIn("succesfully added the review", str(result.data))

    def test_review_get_all(self):
        self.add_business()
        self.client().post(ReviewsTestCase.review_url.format('1'), data=self.review)
        #get reviews for the particular business
        result=self.client().get(ReviewsTestCase.review_url.format('1'))
        self.assertEqual(result.status_code,200)#reviews successfully created

    def test_review_not_exist(self):
        self.add_business()
        #get reviews without adding the reviews
        result=self.client().get(ReviewsTestCase.review_url.format('1'))
        self.assertEqual(result.status_code,404)

    def test_add_review_business_not_exist(self):
        #post review for a business that does not exist
        result=self.client().post(ReviewsTestCase.review_url.format('10'), data=self.review)
        self.assertEqual(result.status_code,404)
        self.assertIn('cannot add review business that does not exist', str(result.data))

    def test_get_review_business_not_exist(self):
        self.add_business()
        self.client().post(ReviewsTestCase.review_url.format('1'), data=self.review)
        #get review for a business that does not exist
        result=self.client().get(ReviewsTestCase.review_url.format('5'))
        self.assertEqual(result.status_code,404)

    def test_add_empty_opinion(self):
        #first add the business
        self.add_business()
        result=self.client().post(ReviewsTestCase.review_url.format('1'), data=self.wrong_review)
        self.assertEqual(result.status_code,400)#bad request
        self.assertIn("make sure the opinion and rating are included", str(result.data))

    def test_add_empty_rating(self):
        #first add the business
        self.add_business()
        result=self.client().post(ReviewsTestCase.review_url.format('1'), data=self.wrong_review)
        self.assertEqual(result.status_code,400)#bad request
        self.assertIn("make sure the opinion and rating are included", str(result.data))
                 
    def tearDown(self):
        """run after every test to ensure database is empty"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()        
