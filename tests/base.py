import unittest
from app import create_app
from app import db


class BaseTestHelper(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        with self.app.app_context():
            # create db tables
            db.create_all()

    def register_user(self, email, password, confirm_password):
        """this method will register a user"""
        user_data = {
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
        return self.client().post('/api/v2/auth/registration', data=user_data)

    def login_user(self, email, password, confirm_password):
        user_data = {
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
        return self.client().post('/api/v2/auth/login', data=user_data)

    def tearDown(self):
        """connect to current context
        and drop all tables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()        