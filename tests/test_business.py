import unittest
import json
from app import db, create_app
from tests.base import BaseTestHelper


class BusinessTestCase(BaseTestHelper):
    """this class tests the business endpoints"""
    # business_endpoints
    register_business = '/api/v2/businesses'
    business_id_url = '/api/v2/businesses/{}'
    user_logout = '/api/v2/auth/log-out'
    wrong_url = '/api/v/businesses'
    paginate_business = '/api/v2/businesses/paginate/1'
    dashboard = '/api/v2/dashboard'
    single_business_dashboard = '/api/v2/dashboard/business/{}'

    def setUp(self):
        """initilize the app
        create test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.business = {'name': 'crastycrab', 'description': 'Fastfood', 'contact': '0702848032', 'category': 'fastfood', 'location': 'atlantic'}
        self.secondBusiness = {'name': 'chumbucket', 'description': 'Fast food restaurant', 'contact': '0702848031', 'category': 'fast food', 'location': 'atlantic'}
        self.business_test = {'name': 'crastycrab', 'description': 'Fast food restaurant', 'category': 'fast food', 'location': 'atlantic'}
        self.business_edit = {'name': 'chumbucket', 'description': 'Fast food restaurant under the sea', 'contact': '0702848032', 'category': 'fast food', 'location': 'atlantic'}
        self.empty_name = {'name': '  ', 'description': 'Fast food restaurant', 'contact': '0702848032', 'category': 'fast food', 'location': 'atlantic'}
        self.empty_update = {'name': '', 'description': 'Fastfood', 'contact': '0702848032', 'category': 'fastfood', 'location': 'atlantic'}
        self.search_param = {'name': 'crastycrab'}
        self.empty_desc = {'name': 'crast', 'contact': '0702848032', 'category': 'fast food', 'location': 'atlantic'}
        self.empty_cont = {'name': 'crasty', 'description': 'Fast food restaurant', 'category': 'fast food', 'location': 'atlantic'}
        self.empty_cat = {'name': 'crasty', 'description': 'Fast food restaurant', 'contact': '0702848032', 'location': 'atlantic'}
        self.empty_loc = {'name': 'crasty', 'description': 'Fast food restaurant', 'contact': '0702848032', 'category': 'fast food'}
        # bind app to current context
        with self.app.app_context():
            # create db tables
            db.create_all()

    def add_business(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        response = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        return response

    def add_second_business(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        response = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.secondBusiness)
        return response

    def test_api_welcome_page(self):
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome to WeConnect", str(response.data))    

    def test_business_creation(self):
        # register a test user and log him in
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        response = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        self.assertIn('crastycrab', str(response.data))

    def test_business_creation_when_user_logged_out(self):
        # register a test user and log him in
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.user_logout, headers=dict(Authorization="Bearer " + access_token), data={"token": access_token})
        response = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 403)
        self.assertIn("You are not logged in. Please log in", str(response.data))

    def test_business_creation_with_token_missing(self):
        """this will test if a user can add a business without a token"""
        response = self.client().post(BusinessTestCase.register_business, data=self.business)
        self.assertEqual(response.status_code, 403)
        self.assertIn("You must have a token to add a business. Login to get a token", str(response.data))
             
    def test_api_can_get_all_businesses(self):
        """this tests if the api can return all bucketlists"""
        # add a business
        self.add_business()
        self.add_second_business()
        result = self.client().get(BusinessTestCase.register_business)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(len(result.data) > 1)

    def test_api_can_get_business_by_id(self):
        # you dont need to be authenticated to view a business
        self.add_business()
        result = self.client().get(BusinessTestCase.business_id_url.format('1'))
        self.assertEqual(result.status_code, 200) 
        self.assertIn('crastycrab', str(result.data))

    def test_api_can_filter_by_category(self):
        # you dont need to be authenticated to view a business
        self.add_business() 
        result = self.client().get(BusinessTestCase.business_id_url.format('fastfood'))
        self.assertEqual(result.status_code, 200) 
        self.assertIn('crastycrab', str(result.data))

    def test_filter_non_existent_category(self):
        """test for filtering with category that does not exist"""
        # you dont need to be authenticated to view a business
        self.add_business() 
        result = self.client().get(BusinessTestCase.business_id_url.format('cars'))
        self.assertEqual(result.status_code, 404) 
        self.assertIn("No business in that category", str(result.data))

    def test_api_can_get_business_by_name(self):
        # you dont need to be authenticated to view or search for a business
        # registers a user and adds a business called crasty crab
        self.add_business() 
        # fill form to search for it
        result = self.client().get('/api/v2/businesses/searches?q=cra')
        # expected request status 
        self.assertEqual(result.status_code, 200)
        # request should return the whole business
        self.assertIn('crastycrab', str(result.data))

    def test_api_response_for_search_not_exist(self):
        # if the user searches an empty field
        # registers a user and adds a business called crasty crab
        self.add_business() 
        # fill form to search for it
        result = self.client().get('/api/v2/businesses/searches?q=ten')
        # expected request status
        self.assertEqual(result.status_code, 404)
        # request should return the whole business
        self.assertIn("No business found", str(result.data))

    def test_api_get_business_does_not_exist(self):
        # add two businesses
        self.add_business()
        self.add_second_business()
        result = self.client().get(BusinessTestCase.business_id_url.format('10'))
        self.assertEqual(result.status_code, 404)

    def test_api_can_update_business(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        edit_response = self.client().put(BusinessTestCase.business_id_url.format('1'), headers=dict(Authorization="Bearer " + access_token), data=self.secondBusiness)
        self.assertEqual(edit_response.status_code, 200)

    def test_unauthorized_user_cannot_update_business(self):
        """you cannot edit a business you did not create"""
        # register and login first user
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # register and login second user
        self.register_user("collinsnjau39@gmail.com", "123test", "123test")
        second_result = self.login_user("collinsnjau39@gmail.com", "123test", "123test")
        # first user add a business
        access_token_first = json.loads(result.data.decode())['access_token']
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token_first), data=self.business)
        # second user tries to update the business
        access_token_second = json.loads(second_result.data.decode())['access_token']
        edit_response = self.client().put(BusinessTestCase.business_id_url.format('1'), headers=dict(Authorization="Bearer " + access_token_second), data=self.secondBusiness)
        self.assertIn("You cannot update a business you did not add", str(edit_response.data))
        self.assertEqual(edit_response.status_code, 401)

    def test_api_cannot_update_business_with_fields_missing(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        edit_response = self.client().put(BusinessTestCase.business_id_url.format('1'), headers=dict(Authorization="Bearer " + access_token), data=self.empty_update)
        self.assertEqual(edit_response.status_code, 400)
        self.assertIn("No field can be empty when updating a business", str(edit_response.data))
        
    def test_api_logged_out_user_cannot_update_business(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)        
        # log out the user
        self.client().post(BusinessTestCase.user_logout, headers=dict(Authorization="Bearer " + access_token), data={"token": access_token})
        edit_response = self.client().put(BusinessTestCase.business_id_url.format('1'), headers=dict(Authorization="Bearer " + access_token), data=self.secondBusiness)
        self.assertEqual(edit_response.status_code, 403)
        self.assertIn("You are not logged in. Please log in", str(edit_response.data))

    def test_api_cannot_update_nonexistent_business(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        edit_response = self.client().put(BusinessTestCase.business_id_url.format('30'), headers=dict(Authorization="Bearer " + access_token), data=self.secondBusiness)
        self.assertEqual(edit_response.status_code, 404)

    def test_api_can_delete_business(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        edit_response = self.client().delete(BusinessTestCase.business_id_url.format('1'), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(edit_response.status_code, 200) 
        result = self.client().get(BusinessTestCase.business_id_url.format('1'))
        self.assertEqual(result.status_code, 404)

    def test_unauthorized_user_cannot_delete_business(self):
        """you cannot delete a business you did not create"""
        # register and login first user
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # register and login second user
        self.register_user("collinsnjau39@gmail.com", "123test", "123test")
        second_result = self.login_user("collinsnjau39@gmail.com", "123test", "123test")
        # first user add a business
        access_token_first = json.loads(result.data.decode())['access_token']
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token_first), data=self.business)
        # second user tries to delete the business
        access_token_second = json.loads(second_result.data.decode())['access_token']
        edit_response = self.client().delete(BusinessTestCase.business_id_url.format('1'), headers=dict(Authorization="Bearer " + access_token_second), data=self.secondBusiness)
        self.assertIn("You cannot delete a business you did not add", str(edit_response.data))
        self.assertEqual(edit_response.status_code, 401)

    def test_logged_out_user_cannot_delete_business(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        # log out the user
        self.client().post(BusinessTestCase.user_logout, headers=dict(Authorization="Bearer " + access_token), data={"token": access_token})
        del_response = self.client().delete(BusinessTestCase.business_id_url.format('1'), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(del_response.status_code, 403)
        self.assertIn("You are not logged in. Please log in", str(del_response.data))
        
    def test_register_business_with_empty_description(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        result = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.empty_desc)
        self.assertEqual(result.status_code, 400)
        self.assertIn("Business description missing", str(result.data))

    def test_register_business_with_empty_category(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        result = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.empty_cat)
        self.assertEqual(result.status_code, 400)
        self.assertIn("Business category missing", str(result.data))

    def test_register_business_with_empty_location(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        result = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.empty_loc)
        self.assertEqual(result.status_code, 400)
        self.assertIn("Business location missing", str(result.data))

    def test_register_business_with_empty_contact(self):
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        result = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.empty_cont)
        self.assertEqual(result.status_code, 400)
        self.assertIn("Business contact missing", str(result.data))                

    def test_register_business_with_name_already_exists(self):
        # register a test user and log him in
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        second_response = self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(second_response.status_code, 409)
        self.assertIn("Business name already exists", str(second_response.data))

    def test_wrong_url(self):
        """test response for wrong url"""
        # add a business
        self.add_business()
        result = self.client().get(BusinessTestCase.wrong_url)
        self.assertEqual(result.status_code, 404)
        self.assertIn("That page does not exist", str(result.data))

    def test_dashboard_returns_right_businesses(self):
        """test if the dashboard endpoint returns the businesses owned by logged in 
        user"""
        # register a test user and log him in
        self.register_user("collins.muru@andela.com", "123test", "123test")
        result = self.login_user("collins.muru@andela.com", "123test", "123test")
        # get the access token
        access_token = json.loads(result.data.decode())['access_token']
        # add the access token to the header
        self.client().post(BusinessTestCase.register_business, headers=dict(Authorization="Bearer " + access_token), data=self.business)
        # access dashboard
        response = self.client().get(BusinessTestCase.dashboard, headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('crastycrab', str(response.data))

    def test_access_dashboard_without_logging_in(self):
        # access dashboard
        response = self.client().get(BusinessTestCase.dashboard)
        self.assertEqual(response.status_code, 403)
        self.assertIn("You must be logged in to access the dashboard", str(response.data))

    def tearDown(self):
        """connect to current context
        and drop all tables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
