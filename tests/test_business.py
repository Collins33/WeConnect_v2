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
        self.business={'name':'crasty crab','description':'Fast food restaurant','contact':'0702848032','category':'fast food','location':'atlantic'}
        self.business_test={'name':'crasty crab','description':'Fast food restaurant','category':'fast food','location':'atlantic'}
        self.business_edit={'name':'chum bucket','description':'Fast food restaurant under the sea','contact':'0702848032','category':'fast food','location':'atlantic'}

        #bind app to current context
        with self.app.app_context():
            #create db tables
            db.create_all()

    def test_business_creation(self):
        response=self.client().post('/api/v2/businesses', data=self.business)
        self.assertEqual(response.status_code,201)

    def test_business_creation_without_all_details(self):
        response=self.client().post('/api/v2/businesses', data=self.business_test)
        self.assertEqual(response.status_code,400)

    def test_api_can_get_all_businesses(self):
        response=self.client().post('/api/v2/businesses', data=self.business)
        self.assertEqual(response.status_code,201)
        res=self.client().get('/api/v2/businesses', data=self.business)
        self.assertEqual(res.status_code,200)

    def test_api_can_get_individual_business(self):
        response=self.client().post('/api/v2/businesses', data=self.business)
        self.assertEqual(response.status_code,201)
        #convert the response to json
        result_in_json=json.loads(response.data.decode('utf-8').replace("'", "\""))

        result=self.client().get('/api/v2/businesses/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code,200)

    def test_api_can_delete_business(self):
        response=self.client().post('/api/v2/businesses', data=self.business)
        self.assertEqual(response.status_code,201)

        result_in_json=json.loads(response.data.decode('utf-8').replace("'", "\""))
        result=self.client().delete('/api/v2/businesses/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code,200)

    def test_api_can_edit_business(self):
        response=self.client().post('/api/v2/businesses', data=self.business)
        self.assertEqual(response.status_code,201)

        result_in_json=json.loads(response.data.decode('utf-8').replace("'", "\""))

        result=self.client().put('/api/v2/businesses/1',data=self.business_edit)
        self.assertEqual(result.status_code,200)

    def test_api_can_get_businesses_location(self):
        response=self.client().post('/api/v2/businesses', data=self.business)
        self.assertEqual(response.status_code,201)
        #convert the response to json
        result_in_json=json.loads(response.data.decode('utf-8').replace("'", "\""))

        result=self.client().get('/api/v2/businesses/{}'.format(result_in_json['location']))
        self.assertEqual(result.status_code,200)

    def test_api_can_get_business_category(self):
        response=self.client().post('/api/v2/businesses', data=self.business)
        self.assertEqual(response.status_code,201)
        #convert the response to json
        result_in_json=json.loads(response.data.decode('utf-8').replace("'", "\""))

        result=self.client().get('/api/v2/businesses/{}'.format(result_in_json['category']))
        self.assertEqual(result.status_code,200)



        










    def tearDown(self):
        """connect to current context
        and drop all tables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()