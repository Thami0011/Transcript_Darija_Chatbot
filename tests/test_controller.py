
import unittest
from fastapi.testclient import TestClient
from app.Controller.Controller import app

client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_root_endpoint(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_chat_endpoint(self):
        response = client.post("/chat", json={"prompt": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())

    def test_voice_endpoint_with_missing_file(self):
        response = client.post("/voice", files={})
        self.assertEqual(response.status_code, 422)  # Expecting a validation error
