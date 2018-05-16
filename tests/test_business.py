import os
import unittest
import json
from app import db, create_app

class BusinessTestCase(unittest.TestCase):
    """this class tests the business endpoints"""

    def setUp(self):
        """initilize the app
        create test variables"""
        self.app=create_app(config_name="testing")
        self.client=self.app.test_client
        self.business=self.business={'name':'crastycrab','description':'Fastfood','contact':'0702848032','category':'fastfood','location':'atlantic'}
        self.secondBusiness={'name':'chumbucket','description':'Fast food restaurant','contact':'0702848031','category':'fast food','location':'atlantic'}
        self.business_test={'name':'crastycrab','description':'Fast food restaurant','category':'fast food','location':'atlantic'}
        self.business_edit={'name':'chumbucket','description':'Fast food restaurant under the sea','contact':'0702848032','category':'fast food','location':'atlantic'}
        self.empty_name={'name':'  ','description':'Fast food restaurant','contact':'0702848032','category':'fast food','location':'atlantic'}

        #bind app to current context
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

    def login_user(self,email="collins.muru@andela.com",password="123test",confirm_password="123test"):
        user_data={
            'email':email,
            'password':password,
            'confirm_password':confirm_password
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

    def add_second_business(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        response=self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.secondBusiness)
        return response


    def test_business_creation(self):
        #register a test user and log him in
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        response=self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        self.assertEqual(response.status_code,201)
        self.assertIn('crastycrab',str(response.data))

    def test_business_creation_user_logged_out(self):
        #register a test user and log him in
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post('/api/v2/auth/log-out',headers=dict(Authorization="Bearer "+ access_token),data={"token":access_token})

        response=self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        self.assertEqual(response.status_code,403)
        self.assertIn("You are not logged in. Please log in",str(response.data))
        

    def test_api_can_get_all_businesses(self):
        """this tests if the api can return all bucketlists"""
        #add a business
        self.add_business()
        result=self.client().get('/api/v2/businesses')
        self.assertEqual(result.status_code,200)

    def test_api_can_get_business_by_id(self):
        #you dont need to be authenticated to view a business
        self.add_business() #registers a user and adds a business
        result=self.client().get('/api/v2/businesses/1')
        self.assertEqual(result.status_code,200) 
        self.assertIn('crastycrab',str(result.data))

    def test_api_get_business_not_exist(self):
        #add two businesses
        self.add_business()
        self.add_second_business()
        result=self.client().get('/api/v2/businesses/10')
        self.assertEqual(result.status_code,404)

    def test_api_can_update_business(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)

        edit_response=self.client().put('/api/v2/businesses/1',headers=dict(Authorization="Bearer "+ access_token),data=self.secondBusiness)
        self.assertEqual(edit_response.status_code,200)

    def test_api_logged_out_user_cannot_update_business(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        
        #log out the user
        self.client().post('/api/v2/auth/log-out',headers=dict(Authorization="Bearer "+ access_token),data={"token":access_token})
        edit_response=self.client().put('/api/v2/businesses/1',headers=dict(Authorization="Bearer "+ access_token),data=self.secondBusiness)
        self.assertEqual(edit_response.status_code,403)
        self.assertIn("You are not logged in. Please log in",str(edit_response.data))

    def test_api_update_nonexistent_business(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        edit_response=self.client().put('/api/v2/businesses/30',headers=dict(Authorization="Bearer "+ access_token),data=self.secondBusiness)
        self.assertEqual(edit_response.status_code,404)

    def test_api_can_delete_business(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)

        edit_response=self.client().delete('/api/v2/businesses/1',headers=dict(Authorization="Bearer "+ access_token))
        self.assertEqual(edit_response.status_code,200)
        
        result=self.client().get('/api/v2/businesses/1')
        self.assertEqual(result.status_code,404)

    def test_logged_out_user_cannot_delete_business(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        #log out the user

        self.client().post('/api/v2/auth/log-out',headers=dict(Authorization="Bearer "+ access_token),data={"token":access_token})
        del_response=self.client().delete('/api/v2/businesses/1',headers=dict(Authorization="Bearer "+ access_token))
        self.assertEqual(del_response.status_code,403)
        self.assertIn("You are not logged in. Please log in",str(del_response.data))
        
    def test_register_business_empty_string(self):
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        result=self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.empty_name)
        self.assertEqual(result.status_code,400)#bad request


    def test_register_business_name_exists(self):
        #register a test user and log him in
        self.register_user()
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        second_response=self.client().post('/api/v2/businesses',headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        self.assertEqual(second_response.status_code,409)
        self.assertIn("Business name already exists", str(second_response.data))

       
           
    def tearDown(self):
        """connect to current context
        and drop all tables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
