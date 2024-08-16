from set_password import app
import unittest
import json


mock_body = {
    "body": json.dumps({
        "username": "imisaelbd",
        "temporary_password": "+>S}Qoer4K}%",
        "new_password": "Misa4258*"
    })
}


class TestApp(unittest.TestCase):
    def test_lambda_handler(self):
        result = app.lambda_handler(mock_body, None)
        print(result)