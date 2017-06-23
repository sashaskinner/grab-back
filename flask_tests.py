import os
import unittest
import tempfile
from server import app


class FlaskTests(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test"""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        """Stuff to do after every test"""
        pass

    def test1(self):
        """Test some portion of the app."""

        result = self.client.get('/')


if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()