import unittest
from unittest.mock import patch
from main import app
from config import not_implemented_ret_code


class TestServer(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_homepage_renders(self):
        # homepage should render HTML template
        response = self.app.get('/')
        self.assertTrue('text/html' in response.content_type)
        self.assertEqual(response.status_code, 200)

    @patch('model_utils.row_to_predictions')
    @patch('model_utils.fetch_model')
    @patch('model_utils.payload_to_row')
    def test_valid_query(self, pl_to_row_mock, fetch_model_mock, r2p_mock):
        # valid queries should get a 200 OK
        pl_to_row_mock.return_value = [], None
        fetch_model_mock.return_value = "example value", None
        r2p_mock.return_value = ["example product"], None

        valid_query_url = "/api/recommender/v1/get_recc?cust_id=1&age=23&gender=F&nationality=NZ&seniority=150&rel_type=ACTIVE&activity_type=ACTIVE&segment=INDIVIDUAL&income=35000"
        response = self.app.get(valid_query_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.json)
        self.assertNotIn("err", response.json)

    def test_field_missing(self):
        # incomplete queries to the API should still return with an error
        # missing a field (in this case income)
        invalid_query_url = "/api/recommender/v1/get_recc?cust_id=1&age=23&gender=F&nationality=NZ&seniority=150&rel_type=ACTIVE&activity_type=ACTIVE&segment=INDIVIDUAL"
        response = self.app.get(invalid_query_url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("err", response.json)

    def test_accept_post_request(self):
        # API supports both GET and POST requests; POST can return a 200 or 400 but should at least go through
        response = self.app.post('/api/recommender/v1/get_recc', json={
            "example_field": "example_value"
        })
        self.assertNotEqual(response.status_code, not_implemented_ret_code)

    def test_404(self):
        response = self.app.get('/not/a/real/path')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
