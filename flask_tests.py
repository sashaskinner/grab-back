import unittest

from server import app
from model import db, create_example_data, connect_to_db


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
        create_example_data()

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

    def test_usjson(self):
        """Test correct data appears at route to us.json"""
        result = self.client.get('us.json')
        self.assertIn = self.client.get('{"type":"Topology",\
            "objects":{"counties":{"type":"GeometryCollection",\
            "bbox"', result.data)

    def test_congressjson(self):
        """Test correct data appears at route to us-congress-113.json"""
        result = self.client.get('us-congress-113.json')
        self.assertIn = self.client.get('{"type":"Topology",\
            "objects":{"districts":{"type":"GeometryCollection"', result.data)

    def test_get_manager(self):
        """Test route """
        pass

    def test_get_employee(self):
        """Test route """
        pass

    def test_chart_manager(self):
        """Test manager chart"""
        result = self.client.get('/chart-data-manager')
        self.assertIn = self.client.get(
            'Districts With Highest %\ Female Employees in Management',
            result.data)

    def test_chart_employee(self):
        """Test chart employee"""
        result = self.client.get('/chart-data-employee')
        self.assertIn = self.client.get(
            'Districts With Highest %\ Female Employees', result.data)

    def test_reverse_employee(self):
        """Test reverse chart employee"""
        result = self.client.get('/chart-data-employee-reverse')
        self.assertIn = self.client.get(
            'Districts With Lowest %\ Female Employees', result.data)

    def test_reverse_manager(self):
        """Test reverse chart manager"""
        result = self.client.get('/chart-data-manager-reverse')
        self.assertIn = self.client.get(
            'Districts With Lowest %\ Female Employees in Management',
            result.data)

    def test_zipcode_lookup(self):
        """Test zipcode look-up"""
        pass


if __name__ == '__main__':
    unittest.main()
