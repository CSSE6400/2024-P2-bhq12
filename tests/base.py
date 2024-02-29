from todo import create_app
import unittest
import os

class ToDoTest(unittest.TestCase):
    def setUp(self):
        os.environ['SQLITE_DB_LOCATION'] = ':memory:'
        self.app = create_app(config_overrides = {'TESTING': True})
        self.client = self.app.test_client()

    def assertDictSubset(self, expected_subset: dict, actual: dict):
        for key, value in expected_subset.items():
            self.assertEqual(actual[key], value)
