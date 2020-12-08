import unittest
from unittest.mock import patch
from model_utils import query_model
from model_utils import fetch_model
from model_utils import payload_to_row
from config import eng_to_esp_inputs
from config import missing_cols


class TestRecommender(unittest.TestCase):
    def test_fetch_invalid_model(self):
        model, err = fetch_model('not/a/real/path')
        self.assertIsNone(model)
        self.assertIsInstance(err, str)


    @patch('model_utils.row_to_predictions')
    @patch('model_utils.fetch_model')
    @patch('model_utils.payload_to_row')
    def test_query_model_valid(self, pl_to_row_mock, fetch_model_mock, r2p_mock):
        """Base case - query goes through if all required input fields are provided"""
        pl_to_row_mock.return_value = [], None
        fetch_model_mock.return_value = "example value", None
        r2p_mock.return_value = ["example product"], None


        valid_payload = {
            'age': "example",
            'gender': "example",
            'nationality': "example",
            'seniority': "example",
            'rel_type': "example",
            'activity_type': "example",
            'segment': "example",
            'income': "example",
        }
        ret_val, err = query_model(valid_payload, 'example_model_path')

        self.assertIsNone(err)
        self.assertEqual(ret_val, ["example product"])

    def test_query_model_missing_params(self):
        """Query fails if params missing"""
        invalid_payload = {
            'age': 5,
            'gender': 5,
            'nationality': 5,
            'seniority': None,
            'rel_type': 5,
            'activity_type': 5,
            'segment': 5,
            'income': 5,
        }
        ret_val, err = query_model(invalid_payload, 'example/model/path')
        self.assertIsNone(ret_val)
        self.assertIsInstance(err, str)

    def test_model_input_formed(self):
        # for a valid input payload from the API, we should get a row for getting predictions from the model
        # that has 40 fields
        example_payload = {
            'cust_id': '35',
            'age': '35',
            'gender': 'F',
            'nationality': 'NZ',
            'seniority': '46',
            'rel_type': 'ACTIVE',
            'activity_type': 'ACTIVE',
            'segment': 'INDIVIDUAL',
            'income': '312000'
        }
        ret, err = payload_to_row(example_payload, eng_to_esp_inputs, missing_cols)
        self.assertIsNone(err)
        expected_row_len = 40
        self.assertEqual(len(ret), expected_row_len)


if __name__ == '__main__':
    unittest.main()
