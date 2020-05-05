from flask import jsonify, request, redirect, url_for, current_app
from flask import Blueprint, request
from flask_login import login_required
from instantApp.extensions import db
from instantApp.models import Chatroom, Message, User
from flask_login import current_user, login_user, login_required, logout_user
from instantApp.utils import generate_token, send_mail_test, send_confirm_account_email, validate_token, resultVo, \
    args_verification, statusVo, send_captcha
from instantApp.settings import Operations
import instantApp.cache_utils as cache
import string, random

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
    mark = request.args.get("mark")  # to see if the user want to use captcha or not
    if not args_verification(name, password, email, mark):
        return statusVo("Arguments mismatch.", "ERROR")
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    if mark == "captcha":
        source = list(string.ascii_letters)
        source.extend(map(lambda x: str(x), range(0, 10)))
        # source.extend(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        captcha = "".join(random.sample(source, 6))  # randomly select 6 digits
        send_captcha(user=user, captcha=captcha)
        cache.set(email, captcha)  # store captcha into cache
        return statusVo("Send captcha success.", "OK")
    else:
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_account_email(user=user, token=token)
        return statusVo("Send confirm email success.", "OK")
        # return redirect(url_for('auth.login', email=email, password=password))


@auth_bp.route('/validate_captcha', methods=['POST'])
def validate_captcha():
    captcha = request.args.get("captcha")
    email = request.args.get("email")
    if not args_verification(captcha, email):
        return statusVo("Arguments mismatch.", "ERROR")
    cache_captcha = cache.get(email)
    if cache_captcha and cache_captcha.lower() == captcha:
        user = User.query.filter(User.email == email).one_or_none()
        if user is None:
            return statusVo("This email has been used.", "ERROR")
        else:
            user.confirm = True
            return statusVo("This user has been confirmed.", "OK")
    else:
        return statusVo("The captcha is not correct", "ERROR")


# @auth_bp.route('/email_captcha')
# def email_captcha():
#     email = request.args.get("email")
#     if not args_verification(email):
#         return statusVo("Arguments mismatch.", "ERROR")
#     source = list(string.ascii_letters)
#     source.extend(map(lambda x: str(x), range(0, 10)))
#     # source.extend(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
#     captcha = "".join(random.sample(source, 6))  # randomly select 6 digits
#     send_captcha()

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
