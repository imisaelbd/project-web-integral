import json
import unittest
from insert_user_pool import app

mock_body = {
    "body": json.dumps({
        "email": "misaelbd@gmail.com",
        "user_name": "imisaelbd",
        "phone_number": "+527771091926",
        "name": "Misael Bahena Diaz",
        "age": 23,
        "gender": "M"
    })
}


class TestApp(unittest.TestCase):
    def test_lambda_handler(self):
        result = app.lambda_handler(mock_body, None)
        print(result)