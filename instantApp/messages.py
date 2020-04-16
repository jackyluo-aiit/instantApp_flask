import requests

from instantApp.extensions import db
from instantApp.models import Chatroom, Message, User
from instantApp.utils import resultVo, args_verification, statusVo
from flask import Blueprint, jsonify, request, redirect, url_for, current_app

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/api/a3/get_chatrooms', methods=["GET"])
def getAllChatrooms():
    result = []
    chatrooms = Chatroom.query.all()
    for each in chatrooms:
        result.append(each.to_json())
    return jsonify(resultVo(result, "OK"))


@messages_bp.route('/api/a3/get_messages', methods=["GET"])
def getMessages():
    result = []
    chatroom_id = request.args.get("chatroom_id")
    page = request.args.get("page")
    if not args_verification(chatroom_id, page):
        return statusVo("Arguments mismatch.", "ERROR")
    page = int(page)
    messages = Message \
        .query \
        .filter(Message.chatroom_id == chatroom_id) \
        .order_by(Message.message_time.desc()) \
        .paginate(page=page, per_page=5, error_out=False)
    for each in messages.items:
        each.message_time = each.message_time.strftime('%Y-%m-%d %H:%M')
        result.append(each.to_json())
    dict = {}
    dict["current_page"] = page
    dict["messages"] = result
    dict["total_pages"] = messages.pages
    return jsonify(resultVo(dict, "OK"))


@messages_bp.route('/api/a3/send_message', methods=["POST"])
def sendMessage():
    url = current_app.config['WEBSOCKET_URL']
    chatroom_id = request.args.get("chatroom_id")
    user_id = request.args.get("user_id")
    name = request.args.get("name")
    message = request.args.get("message")
    if not args_verification(chatroom_id, user_id, name, message):
        return statusVo("Arguments mismatch.", "ERROR")
    message = Message(chatroom_id=chatroom_id, user_id=user_id, name=name, message=message)
    db.session.add(message)
    db.session.commit()
    websocket_message = message.__repr__()
    print(websocket_message)
    res = requests.post(url=url, json=websocket_message)
    result = res.json()
    print(result)
    if result['status'] == 'OK':
        return statusVo("Insert successfully.", "OK")
    else:
        return statusVo("Insert failed.", "ERROR")
