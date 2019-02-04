import unittest
from app import create_app
from instance.config import app_config
from manage import DbSetup


class BaseTest(unittest.TestCase):

    myDb = DbSetup()

    def setUp(self):
        self.app = create_app("testing")
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()

        self.myDb.createTables()

        with self.app_context:
            self.app_context.push()

    correct_signup_payload = {"first_name": "cathy", "last_name": "faith",
                              "other_name": "none", "email": "cath@gmail.com",
                              "phone_number": "123456789",
                              "username": "cathy254", "password": "abdefgh"}

    invalid_signup_payload = {"first": "cathy", "last": "faith",
                              "other": "none", "email": "cath@gmail.com",
                              "phone": "123456789",
                              "user": "cathy254", "password": "abdefgh"}

    empty_data_payload = {"first_name": "", "last_name": "kate",
                          "other_name": "new", "email": "cate@gmail.com",
                          "phone_number": "1212346789",
                          "username": "cathy", "password": "abdefgh"}

    whitespace_signup_payload = {"first_name": " ", "last_name": "faith",
                                 "other_name": "none", "email": " ",
                                 "phone_number": "123456789",
                                 "username": " ", "password": "abdefgh"}

    invalid_email_address = {"first_name": "cathy", "last_name": "faith",
                             "other_name": "none", "email": "cath.com",
                             "phone_number": "123456789",
                             "username": "new254", "password": "abdefgh"}

    invalid_password = {"first_name": "cathy", "last_name": "faith",
                        "other_name": "none", "email": "new@gmail.com",
                        "phone_number": "123456789",
                        "username": "cate254", "password": "abd"}

    email_exists_payload = {"first_name": "catherine", "last_name": "faith",
                            "other_name": "none", "email": "cath@gmail.com",
                            "phone_number": "123456789",
                            "username": "catherine254", "password": "abdefgh"}

    username_exists_payload = {"first_name": "cathy", "last_name": "faith",
                               "other_name": "none", "email": "new_member@gmail.com",
                               "phone_number": "123456789",
                               "username": "cathy254", "password": "abdefgh"}

    username_whitespace_payload = {"first_name": "new", "last_name": "client",
                                   "other_name": "other", "email": "new_client@gmail.com",
                                   "phone_number": "789456123", "username": "new client",
                                   "password": "poiuytrew"}

    def tearDown(self):
        with self.app_context:
            self.app_context.pop()
            self.myDb.drop_tables()
