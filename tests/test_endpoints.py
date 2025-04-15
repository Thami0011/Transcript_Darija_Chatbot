import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.Controller.Controller import app

client = TestClient(app)

class TestEndpoints(unittest.TestCase):
    def test_ping(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "API is running"})
    

    def test_chat_returns_valid_json(self):
        with patch(app.Controller.Controller.generate_response) as mock_generate_response:
            mock_generate_response.return_value = {"response": "Hello", "translation": "Bonjour"}
            response = client.post("/chat", json={"prompt": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("response" in response.json())
        self.assertTrue("translation" in response.json())

    def test_chat_missing_text(self):
        response = client.post("/chat", json={})  # no "text"
        self.assertEqual(response.status_code, 422)

    def test_chat_malformed_json(self):
        headers = {"Content-Type": "application/json"}
        response = client.post("/chat", data="this is not json", headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_transcribe_no_file(self):
        response = client.post("/transcribe", files={})  # no file sent
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    import HtmlTestRunner
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(output='reports', report_name="TestReport", combine_reports=True)
    )
