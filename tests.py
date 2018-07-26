import unittest
import os
import datetime
from application import app
from models import db, User, Message, AdminUser
from create import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        u = User(phone_number='5555555555',
                 display_name='John',
                 location='St. Louis')
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.display_name, 'John')

    def test_create_msg(self):
        cur_time = datetime.datetime.now().strftime("%-m/%d/%Y %-I:%M:%S%p")
        m = Message(message_body='Test msg',
                    message_timestamp=cur_time,
                    message_user_id=1)
        db.session.add(m)
        db.session.commit()
        self.assertEqual(m.message_body, 'Test msg')

    def test_update_name(self):
        u = User(phone_number='5555555555',
                 display_name='John',
                 location='St. Louis')
        db.session.add(u)
        db.session.commit()
        new_name = 'Jimmy'
        user_to_update = User.query.filter_by(
                                    phone_number='5555555555').first()
        user_to_update.display_name = new_name
        db.session.commit()
        self.assertEqual(user_to_update.display_name, new_name)


if __name__ == '__main__':
    unittest.main()
