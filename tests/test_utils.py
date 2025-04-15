
import unittest
from unittest.mock import patch, mock_open
from utils import read_file, generate_response

class TestUtils(unittest.TestCase):

    def test_read_file(self):
        mock_content = "Test content"
        with patch("builtins.open", mock_open(read_data=mock_content)):
            content = read_file("fake_path.txt")
            self.assertEqual(content, mock_content)

    @patch("utils.requests.post")
    def test_generate_response(self, mock_post):
        mock_post.return_value.json.return_value = {"message": {"content": "Hi"}}
        response = generate_response("Hello")
        self.assertIn("Hi", response)
