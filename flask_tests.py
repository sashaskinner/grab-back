import unittest

from server import app


class GrabBackRouteTests(unittest.TestCase):
    """Testing routes in Flask server."""

    def setUp(self):
        """Establish savepoints and backup original session."""
        self.client = app.test_client()
        app.config['TESTING'] = True

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

if __name__ == '__main__':
    unittest.main()
