import unittest

from server import app
from model import db, example_data, connect_to_db


class GrabBackTestCase(unittest.TestCase):
    """Testing routes in Flask server."""

    def setUp(self):
        """ Set up configuration for tests."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Runs at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_index(self):
        """Tests that index route leads to correct html file."""
        result = self.client.get('/')
        self.assertIn('<h3 id="explore">Explore Data</h3>',
                      result.data)

    def test_about(self):
        """Tests that /about leads to correct html file."""
        result = self.client.get('/about')
        self.assertIn('<h1>About</h1>', result.data)
        self.assertIn('I hope that these graphics are useful for visualizing',
                      result.data)

    # add all other routes to test


if __name__ == '__main__':
    unittest.main()
