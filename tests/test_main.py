import unittest
import json
from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_post_review(self):
        # Prepare the test data
        payload = {
            'recipe_id': 1,
            'user_id': 1,
            'text': 'Delicious recipe!',
            'rating': 5,
            'date': '2022-01-01'
        }
        expected_response = {
            'message': 'Review posted successfully'
        }

        # Send a POST request to the endpoint
        response = self.app.post('/post_review', json=payload)

        # Assert the response status code and message
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), expected_response)

        # Additional assertions to verify the review is added to the resource
        # You can add assertions here to check if the review is added to the resource

    def test_hello(self):
        # Send a GET request to the endpoint
        response = self.app.get('/')

        # Assert the response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Hello Review Management!!!\n")

if __name__ == '__main__':
    unittest.main()