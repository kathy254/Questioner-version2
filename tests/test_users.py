import json

from .base_tests import BaseTest
from app.api.models.user_models import Accounts

signup_url = "/api/v2/auth/signup"


class TestUsers(BaseTest):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().setUp()

    def test_create_account(self):
        response = self.test_client.post(signup_url,
                                         data=json.dumps(self.correct_signup_payload),
                                         content_type="application/json")
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["status"], 201)
        self.assertEqual(result["message"], "Account with username cathy254\
                                            created successfully.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.content_type == "application/json")

    def test_invalid_signup_payload(self):
        response1 = self.test_client.post(signup_url,
                                          data=json.dumps(self.invalid_signup_payload),
                                          content_type="application/json")
        result1 = json.loads(response1.data.decode("UTF-8"))

        self.assertEqual(result1["status"], 400)
        self.assertEqual(result1["message"], "Payload is invalid")
        self.assertEqual(response1.status_code, 400)
        self.assertTrue(response1.content_type == "application/json")

    def test_empty_data(self):
        response2 = self.test_client.post(signup_url,
                                          data=json.dumps(self.empty_data_payload),
                                          content_type="application/json")
        result2 = json.loads(response2.data.decode("UTF-8"))

        self.assertEqual(result2["status"], 400)
        self.assertEqual(result2["message"], "Data set cannot be empty.")
        self.assertEqual(response2.status_code, 400)
        self.assertTrue(response2.content_type == "application/json")

    def test_whitespace_payload(self):
        response3 = self.test_client.post(signup_url,
                                          data=json.dumps(self.whitespace_signup_payload),
                                          content_type="application/json")
        result3 = json.loads(response3.data.decode("UTF-8"))

        self.assertEqual(result3["status"], 400)
        self.assertEqual(result3["message"], "Data cannot contain whitespaces only")
        self.assertEqual(response3.status_code, 400)
        self.assertTrue(response3.content_type == "application/json")

    def test_invalid_email_payload(self):
        response4 = self.test_client.post(signup_url,
                                          data=json.dumps(self.invalid_email_address),
                                          content_type="application/json")
        result4 = json.loads(response4.data.decode("UTF-8"))

        self.assertEqual(response4["status"], 400)
        self.assertEqual(result4["message"], "Please enter a valid email address.")
        self.assertEqual(response4.status_code, 400)
        self.assertTrue(response4.content_encoding == "application/json")

    def test_invalid_password(self):
        response5 = self.test_client.post(signup_url,
                                          data=json.dumps(self.invalid_password),
                                          content_type="application/json")
        result5 = json.loads(response5.data.decode("UTF-8"))

        self.assertEqual(result5["status"], 400)
        self.assertEqual(result5["message"], "Password must be at least 6\
                         characters long without white spaces")
        self.assertEqual(response5.status_code, 400)
        self.assertTrue(response5.content_type == "application/json")

    def test_invalid_username(self):
        response9 = self.test_client.post(signup_url,
                                          data=json.dumps(self.username_whitespace_payload),
                                          content_type = "application/json")
        result9 = json.loads(response9.data.decode("UTF-8"))

        self.assertEqual(result9["status"], 400)
        self.assertEqual(result9["message"], "Username cannot contains whitespaces.")
        self.assertEqual(response9.status_code, 400)
        self.assertTrue(response9.content_type == "application/json")

    def test_email_exists(self):
        self.test_client.post(signup_url,
                              data=json.dumps(self.correct_signup_payload),
                              content_type="application/json")

        response6 = self.test_client.post(signup_url,
                                          data=json.dumps(self.email_exists_payload),
                                          content_type="application/json")
        result6 = json.loads(response6.data.decode("UTF-8"))

        self.assertEqual(result6["status"], 400)
        self.assertEqual(result6["message"], "This email address already exists.\
                                 Please sign in.")
        self.assertEqual(response6.status_code, 400)
        self.assertTrue(response6.content_type == "application/json")

    def test_username_exists(self):
        self.test_client.post(signup_url,
                              data=json.dumps(self.correct_signup_payload),
                              content_type="application/json")

        response7 = self.test_client.post(signup_url,
                                          data=json.dumps(self.username_exists_payload),
                                          content_type="application/json")
        result7 = json.loads(response7.data.decode("UTF-8"))

        self.assertEqual(result7["status"], 400)
        self.assertEqual(result7["message"], "This username already exists.\
                                 Please choose another one.")
        self.assertEqual(response7.status_code, 400)
        self.assertTrue(response7.content_type == "application/json")

    def test_server_error(self):
        response8 = self.test_client.post(signup_url,
                                          data=json.dumps(self),
                                          content_type="application/json")
        result8 = json.loads(response8.data.decode("UTF-8"))

        self.assertEqual(result8["message"], "Internal Server Error")
        self.assertEqual(response8.status_code, 500)
