import os

import requests

from instantApp.extensions import db
from instantApp.models import Chatroom, Message, User, File
from instantApp.utils import resultVo, args_verification, statusVo, allowed_file
from flask import Blueprint, jsonify, request, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename

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


@messages_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    url = current_app.config['SENDFILE_URL']
    if request.method == 'POST':
        file = request.files['file']  # input key-value parameter
        uploader = request.args.get("name")  # the name of the user
        uploader_id = request.args.get("user_id")
        chatroom_id = request.args.get("chatroom_id")
        if file and allowed_file(file.filename) and args_verification(uploader, chatroom_id):
            filename = secure_filename(file.filename)
            filepath = os.path.join(os.path.dirname(current_app.root_path), upload_folder)
            filepath = os.path.join(filepath, filename)
            file.save(filepath)
            f = File(file_name=filename, file_path=filepath, uploader_id=int(uploader_id))
            db.session.add(f)
            db.session.commit()
            websocket_message = f.__repr__()
            websocket_message["username"] = uploader
            websocket_message["chatroom_id"] = chatroom_id
            websocket_message["api_path"] = url_for("messages.download", filename=filename)
            res = requests.post(url=url, json=websocket_message)
            result = res.json()
            print(result)
            if result['status'] == 'OK':
                return statusVo("Send file successfully.", "OK")
            else:
                return statusVo("Send file failed.", "ERROR")
        else:
            return statusVo("Upload Failed.", "ERROR")
    else:
        return statusVo("Upload Failed.", "ERROR")


@messages_bp.route('/upload/<filename>')
def download(filename):
    print(filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    # filename = request.args.get("filename")
    if request.method == 'GET' and args_verification(filename):
        uploads = os.path.join(os.path.dirname(current_app.root_path), upload_folder)
        if os.path.isfile(os.path.join(uploads, filename)):
            return send_from_directory(uploads, filename, as_attachment=True)
        else:
            return statusVo("File does not exist.", "ERROR")
    else:
        return statusVo("Method mismatch.", "ERROR")
