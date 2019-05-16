import os
from flask import (Flask, session,
                   render_template, url_for, redirect, request, jsonify)
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import json
from models import db, User, Message, AdminUser
from create import create_app


app = create_app()
socketio = SocketIO(app)
app.app_context().push()


# Routes
@app.route("/", methods=['POST', 'GET'])
def index():

    is_admin = session.get('admin')
    all_users_list = []
    all_messages_list = []
    all_users = User.get_all_users()
    all_messages = Message.get_all_messages()

    for user in all_users:
        all_user_dict = {}
        all_user_dict['user'] = user
        all_user_dict['text_count'] = User.user_total_texts(user.id)
        all_users_list.append(all_user_dict)

    return render_template('textline.html',
                           all_users=all_users_list,
                           all_messages=all_messages,
                           is_admin=is_admin,
                           total_texts=len(all_messages))


@app.route("/all_single_user_messages", methods=['POST'])
def all_single_user_messages():
    all_user_messages = Message.get_all_user_messages(
                                            request.form['user_id_clicked'])
    all_user_messages_list = []
    for msg in all_user_messages:
        all_user_messages_dict = {}
        all_user_messages_dict['user'] = msg[1].display_name
        all_user_messages_dict['number'] = msg[1].phone_number
        all_user_messages_dict['msg_body'] = msg[0].message_body
        all_user_messages_dict['timestamp'] = msg[0].message_timestamp
        all_user_messages_dict['message_media_url'] = msg[0].message_media_url
        all_user_messages_list.append(all_user_messages_dict)
    return jsonify(all_user_messages_list)


@app.route("/search_for_user", methods=['POST'])
def search_for_user():
    all_searched_users_list = []
    search_term = request.form['search_term']
    users = User.query.filter(
                            User.display_name.ilike("%"+search_term+"%") |
                            User.phone_number.ilike("%"+search_term+"%")).all()
    for user in users:
        all_searched_users_dict = {}
        all_searched_users_dict['user'] = user.display_name
        all_searched_users_dict['user_id'] = user.id
        all_searched_users_dict['number'] = user.phone_number
        all_searched_users_dict['location'] = user.location
        all_searched_users_dict['text_count'] = User.user_total_texts(user.id)
        all_searched_users_list.append(all_searched_users_dict)
    return jsonify(all_searched_users_list)


@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    error_message = ""
    if request.method == 'POST':
        password_attempt = request.form['admin_password']
        password = db.session.query(AdminUser.password).first()
        print(password_attempt)
        if password_attempt == password[0]:
            session['admin'] = True
            return redirect(url_for('index'))
        else:
            error_message = "Incorrect Password"
            return render_template('admin_login.html',
                                   error_message=error_message)
    return render_template('admin_login.html')


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


@app.route('/sms', methods=['POST'])
def sms():
    phone_number = request.form['From'][2:]
    message_body = request.form['Body']
    from_city = request.form['FromCity']
    from_state = request.form['FromState']
    timestamp = datetime.datetime.now().strftime("%-m/%d/%Y %-I:%M:%S%p")
    default_name = "The " + phone_number[:3]
    location = f"{from_city}, {from_state}"
    num_media = int(request.form['NumMedia'])

    user = User.query.filter_by(phone_number=phone_number).first()

    if user is None:
        user = User(phone_number=phone_number,
                    display_name=default_name,
                    location=location)
        db.session.add(user)
        db.session.commit()
        does_user_exist = False
    else:
        does_user_exist = True

    message = Message(message_body=message_body,
                      message_timestamp=timestamp,
                      message_user_id=user.id)
    if num_media > 0:
        media = request.form["MediaUrl0"]
        message.message_media_url = media
    db.session.add(message)
    db.session.commit()

    new_text = {
        "message": message.to_dict(),
        "user": user.to_dict(),
        "does_user_exist": does_user_exist,
        "total_texts_from_user": User.user_total_texts(user.id),
    }

    socketio.emit('msg received', new_text, broadcast=True)
    resp = MessagingResponse()
    resp.message("Your message has been sent to The Text Inbox")
    return str(resp)


@app.route('/update_name', methods=['POST'])
def update_name():
    new_name = request.form['new_name']
    number_to_update = request.form['number_to_update']
    user_to_update = User.query.filter_by(
                                         phone_number=number_to_update).first()
    user_to_update.display_name = new_name
    db.session.commit()
    return redirect(url_for('index'))


@app.before_request
def make_session_permanent():
    session.permanent = True
