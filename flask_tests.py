import server
import unittest


class MyAppIntegrationTestCase(unittest.TestCase):
    """Testing routes in Flask server."""

    def setUp(self):
        """ Set up configuration for tests."""
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

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

if __name__ == '__main__':
    unittest.main()
