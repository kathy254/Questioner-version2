import unittest
from app import create_app
from manage import DbSetup
from instance.config import app_config


class BaseTest(unittest.TestCase):

    myDb = DbSetup()

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.myDb.createTables()

        with self.app_context:
            self.app_context.push()

    def tearDown(self):
        with self.app_context:
            self.app_context.pop()
            self.myDb.drop_tables()

    