from flask import jsonify, request, redirect, url_for, current_app
from flask import Blueprint, request
from flask_login import login_required
from instantApp.extensions import db
from instantApp.models import Chatroom, Message, User
from flask_login import current_user, login_user, login_required, logout_user
from instantApp.utils import generate_token, send_mail_test, send_confirm_account_email, validate_token, resultVo, args_verification, statusVo
from instantApp.settings import Operations

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    # id = request.args.get("id")
    email = request.args.get("email")
    password = request.args.get("password")
    if not args_verification(email, password):
        return statusVo("Arguments mismatch.", "ERROR")
    if current_user.is_authenticated:
        return statusVo("Verification success.", "OK")
    user = User.query.filter(User.email == email).first()
    if user:
        if user.validate_password(password):
            login_user(user)
            return statusVo("Verification success.", "OK")
        else:
            return statusVo("Verification failed.", "ERROR")
    else:
        return statusVo("User does't exist.", "ERROR")


@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.args.get("name")
    password = request.args.get("password")
    email = request.args.get("email")
    if not args_verification(name, password, email):
        return statusVo("Arguments mismatch.", "ERROR")
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    token = generate_token(user=user, operation=Operations.CONFIRM)
    send_confirm_account_email(user=user, token=token)
    return redirect(url_for('auth.login', email=email, password=password))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return statusVo("Logout success.", "OK")


@auth_bp.route('/confirm/<token>')
def confirm(token):
    if validate_token(token=token, operation=Operations.CONFIRM):
        return statusVo("Confirm success.", "OK")
    else:
        return statusVo("Confirm failed.", "OK")


@auth_bp.route('/test_mail', methods=['GET'])
def mail_test():
    send_mail_test()
    return statusVo("Send mail, please check.", "OK")
