import os

import requests, time

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
    # messages = Message \
    #     .query \
    #     .filter(Message.chatroom_id == chatroom_id) \
    #     .order_by(Message.message_time.desc()) \
    #     .paginate(page=page, per_page=5, error_out=False)
    messages = db.session.query(Message.id, Message.chatroom_id, Message.user_id, Message.name, Message.message,
                                Message.message_time, Message.type, File.id, File.file_name,
                                File.file_path).outerjoin(File, Message.file_id == File.id).order_by(
        Message.message_time.desc()).paginate(page=page, per_page=5, error_out=False)
    for each in messages.items:
        (message_id, chatroom_id, user_id, name, message, message_time, type, file_id, filename, file_path) = each
        api_path = None
        if type != 1:
            api_path = url_for("messages.download", filename=filename)
        each = {"message_id": message_id, "chatroom_id": chatroom_id, "user_id": user_id, "name": name,
                "message": message, "message_time": message_time, "type": type, "file_id": file_id,
                "filename": filename, "file_path": file_path,
                "api_path": api_path}
        each["message_time"] = each["message_time"].strftime('%Y-%m-%d %H:%M')
        result.append(each)
    dict = {}
    dict["current_page"] = page
    dict["messages"] = result
    dict["total_pages"] = messages.pages
    return jsonify(resultVo(dict, "OK"))


@messages_bp.route('/api/a3/send_message', methods=["POST"])
def sendMessage():
    url = current_app.config['WEBSOCKET_URL']
    chatroom_id = request.form.get("chatroom_id")
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    message = request.form.get("message")
    if not args_verification(chatroom_id, user_id, name, message):
        return statusVo("Arguments mismatch.", "ERROR")
    chatroom = Chatroom.query.filter(Chatroom.id == chatroom_id).one_or_none()
    message = Message(chatroom_id=chatroom_id, user_id=user_id, name=name, message=message)
    db.session.add(message)
    db.session.commit()
    websocket_message = message.__repr__()
    websocket_message['chatroom_name'] = chatroom.name
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
        type = request.args.get("type")
        if file and allowed_file(file.filename) and args_verification(uploader, chatroom_id):
            filename = secure_filename(file.filename)
            (filename, extension) = os.path.splitext(filename)
            filename = filename + '_' + uploader + '_' + str(int(time.time())) + extension
            filepath = os.path.join(os.path.dirname(current_app.root_path), upload_folder)
            filepath = os.path.join(filepath, filename)
            file.save(filepath)
            m = Message(chatroom_id=chatroom_id, user_id=uploader_id, name=uploader, type=type)
            f = File(file_name=filename, file_path=filepath, uploader_id=uploader_id)
            db.session.add(f)
            db.session.add(m)
            f.messages.append(m)
            db.session.commit()
            websocket_message = {"message_id": m.id, "chatroom_id": chatroom_id, "user_id": uploader_id,
                                 "name": uploader,
                                 "message": m.message, "message_time": m.message_time.strftime('%Y-%m-%d %H:%M'),
                                 "type": type, "file_id": m.id,
                                 "filename": filename, "file_path": filepath,
                                 "api_path": url_for("messages.download", filename=filename)}
            # websocket_message = f.__repr__()
            # websocket_message["name"] = uploader
            # websocket_message["type"] = type
            # websocket_message["chatroom_id"] = chatroom_id
            # websocket_message["api_path"] = url_for("messages.download", filename=filename)
            print(websocket_message)
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
