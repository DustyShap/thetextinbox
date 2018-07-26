import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, desc


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

    def get_all_users():
        return db.session.query(User).join(Message, User.id==Message.message_user_id).order_by(desc(Message.id)).all()

    def user_total_texts(user_id):
        return Message.query.filter_by(message_user_id=user_id).count()


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

    def get_all_messages():
        return db.session.query(Message,User).join(User, Message.message_user_id == User.id).order_by(desc(Message.id)).all()

    def get_all_user_messages(user_id):
        return db.session.query(Message,User).join(User,Message.message_user_id == User.id).filter(User.id == user_id).order_by(desc(Message.id)).all()



class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String,nullable=False)
