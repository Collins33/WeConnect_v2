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

        #bind app to current context
        with self.app.app_context():
            #create db tables
            db.create_all()

