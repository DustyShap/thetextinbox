import unittest
import os
from application import app


class BasicTests(unittest.TestCase):
    def test_main_page(self):
        self.app = app.test_client()
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
