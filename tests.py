import unittest
import os
from application import app
from create import *
from models import *


class BasicTests(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        self.app = app.test_client()
        # db.create_all()


    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def test_admin_login(self):
        res = self.app.get("/admin_login")
        self.assertEqual(res.status_code,200)

    # def test_main_page(self):
    #     self.app = create_app()
    #     response = self.app.get("/")
    #     self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
