import unittest
import json
from app import app

class ScrollSageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test that the home page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ScrollSage', response.data)

    def test_insights_endpoint_no_data(self):
        """Test insights endpoint with no data"""
        response = self.app.post('/insights', 
                               data=json.dumps({}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_insights_endpoint_empty_entities(self):
        """Test insights endpoint with empty entities list"""
        response = self.app.post('/insights',
                               data=json.dumps({'entities': []}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_insights_endpoint_invalid_data(self):
        """Test insights endpoint with invalid data structure"""
        response = self.app.post('/insights',
                               data=json.dumps({'entities': [{'name': 'test'}]}),
                               content_type='application/json')
        # This should fail due to missing API keys in test environment
        self.assertIn(response.status_code, [400, 500])

if __name__ == '__main__':
    unittest.main() 