import os
from flask_sqlalchemy import SQLAlchemy
from application import *

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
                    "phone_number": self.phone_number,
                    "display_name":self.display_name,
                    "location":self.location,
                    "user_id":self.id,
                }

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    message_body = db.Column(db.String, nullable=False)
    message_timestamp = db.Column(db.String,nullable=False)
    message_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message_media_url = db.Column(db.String, nullable=True)

    def to_dict(self):
            return {
                "user_id":self.message_user_id,
                "message_body":self.message_body,
                "timestamp":self.message_timestamp,
                'media':self.message_media_url,
            }

class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String,nullable=False)
