import unittest

from .base_tests import BaseTest
from app.api.utils.validations import Validations


class TestValidations(BaseTest):

    def setUp(self):
        super().setUp()
        self.test = Validations()

    def tearDown(self):
        super().tearDown()
        self.test = None

    def test_empty_data(self):
        data = self.test.is_empty(["", "abcd"])
        self.assertTrue(data)

    def test_data_not_empty(self):
        data = self.test.is_empty(["abcd", "abcd"])
        self.assertFalse(data)

    def test_data_white_space_only(self):
        data = self.test.is_whitespace_only([" ", "abcd"])
        self.assertTrue(data)

    def test_not_white_space_only(self):
        data = self.test.is_whitespace_only(["abcd", "abcd"])
        self.assertFalse(data)

    def test_whitespace_exists(self):
        data = self.test.is_whitespace_exists(["my name", "is me"])
        self.assertTrue(data)

    def test_not_whitespace_exists(self):
        data = self.test.is_whitespace_only(["myname", "isme"])
        self.assertFalse(data)

    def test_is_string(self):
        data = self.test.is_string("this is a string")
        self.assertTrue(data)

    def test_not_string(self):
        data = self.test.is_string([1, 2, 3, 4])
        self.assertFalse(data)

    def test_is_integer(self):
        data = self.test.is_integer([1, 2, 3, 4])
        self.assertTrue(data)

    def test_not_integer(self):
        data1 = self.test.is_integer(["this is", "not me"])
        data2 = self.test.is_integer([2.13, 3.21])
        self.assertFalse(data1)
        self.assertFalse(data2)

    def test_valid_email(self):
        email = self.test.valid_email("email@gmail.com")
        email_country = self.test.valid_email("email@yahoo.co.uk")
        email_long_tld = self.test.valid_email("email@yahoo.travel")
        email_capital = self.test.valid_email("EMAIL@GMAIL.COM")
        self.assertTrue(email)
        self.assertTrue(email_country)
        self.assertTrue(email_long_tld)
        self.assertTrue(email_capital)

    def test_invalid_email(self):
        data1 = self.test.valid_email("abcdefg")
        data2 = self.test.valid_email("gmail.com")
        self.assertFalse(data1)
        self.assertFalse(data2)

    def test_valid_password(self):
        data1 = self.test.valid_password("123skikdos")
        data2 = self.test.valid_password("ASI92@#as8*i")
        self.assertTrue(data1)
        self.assertTrue(data2)

    def test_invalid_password(self):
        data1 = self.test.valid_password("jaj jsj")
        data2 = self.test.valid_password("1234")
        self.assertFalse(data1)
        self.assertFalse(data2)

    def test_valid_signup_payload(self):
        payload = {"first_name": "me", "last_name": "none",
                   "other_name": "none", "email": "email@gmail.com",
                   "phone_number": "123456789", "username": "new_user",
                   "password": "abcdefghs"}
        data = self.test.valid_signup_payload(payload)
        self.assertTrue(data)

    def test_invalid_signup_payload(self):
        payload1 = {"first_name": "my_name", "why": "new_user"}
        payload2 = {"first": "cath", "last": "faith", "other": "none",
                    "email_address": "new@yahoo.com", "phone": "123654987",
                    "username": "none_user", "pass": "1234"}
        data1 = self.test.valid_signup_payload(payload1)
        data2 = self.test.valid_signup_payload(payload2)
        self.assertFalse(data1)
        self.assertFalse(data2)

    def test_valid_login_payload(self):
        payload = {"username": "new_member", "password": "qwertyuiop"}
        data = self.test.valid_login_payload(payload)
        self.assertTrue(data)

    def test_invalid_login_payload(self):
        payload1 = {"username": "new", "none": "none"}
        payload2 = {"user": "member", "pass": "poiie"}
        data1 = self.test.valid_login_payload(payload1)
        data2 = self.test.valid_login_payload(payload2)
        self.assertFalse(data1)
        self.assertFalse(data2)
