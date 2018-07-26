import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from models import *



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    socketio = SocketIO(app)
    return app

# db.init_app(app)

def main():
    db.create_all()


if __name__ == '__main__':
    with app.app_context():
        main()
