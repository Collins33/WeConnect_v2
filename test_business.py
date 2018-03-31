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






    def tearDown(self):
        """connect to current context
        and drop all tables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
