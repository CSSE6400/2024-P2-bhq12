from todo import create_app
import unittest
import os

class TodoTest(unittest.TestCase):
    def setUp(self):

        os.environ['SQLITE_DB_LOCATION'] = 'unit_test.db'
        self.app = create_app(config_overrides = {'TESTING': True})
        self.client = self.app.test_client()

    def assertDictSubset(self, expected_subset: dict, actual: dict):
        for key, value in expected_subset.items():
            self.assertEqual(actual[key], value)
