import os
import unittest
import json
from app import db, create_app

class BusinessTestCase(unittest.TestCase):
    """this class tests the business endpoints"""
    #business_endpoints
    register_business='/api/v2/businesses'
    business_id_url='/api/v2/businesses/{}'
    user_logout='/api/v2/auth/log-out'

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
        self.empty_update={'name':'','description':'Fastfood','contact':'0702848032','category':'fastfood','location':'atlantic'}
        self.search_param={'name':'crastycrab'}
        #bind app to current context
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

    def login_user(self,email="collins.muru@andela.com",password="123test",confirm_password="123test"):
        user_data={
            'email':email,
            'password':password,
            'confirm_password':confirm_password
        }
        return self.client().post('/api/v2/auth/login',data=user_data)
                

    def add_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        response=self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        return response

    def add_second_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        response=self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.secondBusiness)
        return response


    def test_business_creation(self):
        #register a test user and log him in
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        response=self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        self.assertEqual(response.status_code,201)
        self.assertIn('crastycrab',str(response.data))

    def test_business_creation_when_user_logged_out(self):
        #register a test user and log him in
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post(BusinessTestCase.user_logout,headers=dict(Authorization="Bearer "+ access_token),data={"token":access_token})

        response=self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        self.assertEqual(response.status_code,403)
        self.assertIn("You are not logged in. Please log in",str(response.data))
        

    def test_api_can_get_all_businesses(self):
        """this tests if the api can return all bucketlists"""
        #add a business
        self.add_business()
        result=self.client().get(BusinessTestCase.register_business)
        self.assertEqual(result.status_code,200)

    def test_api_can_get_business_by_id(self):
        #you dont need to be authenticated to view a business
        self.add_business() #registers a user and adds a business
        result=self.client().get(BusinessTestCase.business_id_url.format('1'))
        self.assertEqual(result.status_code,200) 
        self.assertIn('crastycrab',str(result.data))

    def test_api_can_filter_by_category(self):
        #you dont need to be authenticated to view a business
        self.add_business() #registers a user and adds a business
        result=self.client().get(BusinessTestCase.business_id_url.format('fastfood'))
        self.assertEqual(result.status_code,200) 
        self.assertIn('crastycrab',str(result.data))

    def test_filter_non_existent_category(self):
        """test for filtering with category that does not exist"""
        #you dont need to be authenticated to view a business
        self.add_business() #registers a user and adds a business
        result=self.client().get(BusinessTestCase.business_id_url.format('cars'))
        self.assertEqual(result.status_code,404) 
        self.assertIn("No business in that category",str(result.data))

    def test_api_can_get_business_by_name(self):
        #you dont need to be authenticated to view or search for a business
        self.add_business() #registers a user and adds a business called crasty crab
        result=self.client().post('/api/v2/businesses/search', data=self.search_param)# fill form to search for it
        self.assertEqual(result.status_code,200)#expected request status 
        self.assertIn('crastycrab',str(result.data))# request should return the whole business

    def test_search_with_empty_field(self):
        #if the user searches an empty field
        self.add_business() #registers a user and adds a business called crasty crab
        result=self.client().post('/api/v2/businesses/search', data={'name':''})# fill form to search for it
        self.assertEqual(result.status_code,400)#expected request status 
        self.assertIn('please enter name to search',str(result.data))# request should return the whole business

    def test_api_response_for_search_not_exist(self):
        #if the user searches an empty field
        self.add_business() #registers a user and adds a business called crasty crab
        result=self.client().post('/api/v2/businesses/search', data={'name':'apple'})# fill form to search for it
        self.assertEqual(result.status_code,404)#expected request status 
        self.assertIn('Sorry but the business could not be found',str(result.data))# request should return the whole business

    def test_api_get_business_does_not_exist(self):
        #add two businesses
        self.add_business()
        self.add_second_business()
        result=self.client().get(BusinessTestCase.business_id_url.format('10'))
        self.assertEqual(result.status_code,404)

    def test_api_can_update_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)

        edit_response=self.client().put(BusinessTestCase.business_id_url.format('1'),headers=dict(Authorization="Bearer "+ access_token),data=self.secondBusiness)
        self.assertEqual(edit_response.status_code,200)

    def test_api_cannot_update_business_with_fields_missing(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        edit_response=self.client().put(BusinessTestCase.business_id_url.format('1'),headers=dict(Authorization="Bearer "+ access_token),data=self.empty_update)
        self.assertEqual(edit_response.status_code,400)
        self.assertIn("No field can be empty when updating a business",str(edit_response.data))
        
    def test_api_logged_out_user_cannot_update_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)        
        #log out the user
        self.client().post(BusinessTestCase.user_logout,headers=dict(Authorization="Bearer "+ access_token),data={"token":access_token})
        edit_response=self.client().put(BusinessTestCase.business_id_url.format('1'),headers=dict(Authorization="Bearer "+ access_token),data=self.secondBusiness)
        self.assertEqual(edit_response.status_code,403)
        self.assertIn("You are not logged in. Please log in",str(edit_response.data))

    def test_api_cannot_update_nonexistent_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        edit_response=self.client().put(BusinessTestCase.business_id_url.format('30'),headers=dict(Authorization="Bearer "+ access_token),data=self.secondBusiness)
        self.assertEqual(edit_response.status_code,404)

    def test_api_can_delete_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        edit_response=self.client().delete(BusinessTestCase.business_id_url.format('1'),headers=dict(Authorization="Bearer "+ access_token))
        self.assertEqual(edit_response.status_code,200) 
        result=self.client().get(BusinessTestCase.business_id_url.format('1'))
        self.assertEqual(result.status_code,404)

    def test_logged_out_user_cannot_delete_business(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        #log out the user
        self.client().post(BusinessTestCase.user_logout,headers=dict(Authorization="Bearer "+ access_token),data={"token":access_token})
        del_response=self.client().delete(BusinessTestCase.business_id_url.format('1'),headers=dict(Authorization="Bearer "+ access_token))
        self.assertEqual(del_response.status_code,403)
        self.assertIn("You are not logged in. Please log in",str(del_response.data))
        
    def test_register_business_with_empty_string(self):
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        result=self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.empty_name)
        self.assertEqual(result.status_code,400)#bad request

    def test_register_business_with_name_already_exists(self):
        #register a test user and log him in
        self.register_user("collins.muru@andela.com","123test","123test")
        result=self.login_user()
        #get the access token
        access_token=json.loads(result.data.decode())['access_token']
        #add the access token to the header
        self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
        second_response=self.client().post(BusinessTestCase.register_business,headers=dict(Authorization="Bearer "+ access_token) ,data=self.business)
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
