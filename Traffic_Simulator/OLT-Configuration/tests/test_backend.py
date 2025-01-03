import unittest
from backend.api import app


class TestBackend(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_data(self):
        response = self.app.get("/api/data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"key": "Hello from the backend!"})


if __name__ == "__main__":
    unittest.main()
