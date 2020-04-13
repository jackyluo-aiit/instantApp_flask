from instantApp.extensions import socketio
from instantApp.models import Message
from flask_socketio import emit
from flask import Blueprint, render_template

chats_bp = Blueprint('chats', __name__)


@chats_bp.route('/test')
def get_test():
    return render_template('test.html')


@chats_bp.route('/push')
def new_message():
    # message = Message(author=current_user._get_current_object(), body=message_body)
    # db.session.add(message)
    # db.session.commit()
    # emit('new message',
    #      {'response': 'hi'},
    #      broadcast=True)
    print('sending')
    event_name = 'new message'
    broadcasted_data = {'data': "pushed once!"}
    socketio.emit(event_name, broadcasted_data, broadcast=True)
    return 'done!'


@socketio.on('new message')
def new_message(message_body):
    print(message_body)


@socketio.on('connect')
def connect():
    # global online_users
    # if current_user.is_authenticated and current_user.id not in online_users:
    #     online_users.append(current_user.id)
    #
    print('connected')


@socketio.on('disconnect')
def disconnect_msg():
    """socket client event - disconnected"""
    print('client disconnected!')
