from threading import Thread

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, render_template
from flask_mail import Message
from instantApp import mail, db
from instantApp.models import User
from instantApp.settings import Operations


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(token, operation):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    id = data.get('id')
    user = User.query.get(int(id))
    if user.confirm:
        return True
    if operation != data.get('operation') or user.id != user.id:
        return False
    if operation == Operations.CONFIRM:
        user.confirm = True
    else:
        return False
    db.session.commit()
    return True


def send_confirm_account_email(user, token):
    send_mail(subject='Email Confirm', to=user.email, template='emails/confirm', user=user, token=token)


def send_captcha(user, captcha):
    send_mail(subject='Email Captcha', to=user.email, template='emails/captcha_confirm', captcha=captcha)


# def send_email_captcha(user):
#     mc = memcache.Client(['127.0.0.1:12000'], debug=False)
#     captcha = str(uuid.uuid1())[:6]
#     mc.set(user.email, captcha)
#     message = Message('instantApp verification code', recipients=[user.email],
#                       body='Your verification code: %s' % captcha)
#     app = current_app._get_current_object()
#     thr = Thread(target=_send_async_mail, args=[app, message])
#     thr.start()
#     return thr


def send_mail(subject, to, template, **kwargs):
    message = Message(subject, recipients=[to])
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail_test():
    message = Message(subject='Hello World', recipients=['jackyluo0412@gmail.com'], body='Hello')
    mail.send(message)


def resultVo(data, status):
    dict = {}
    dict["data"] = data
    dict["status"] = status
    return dict


def statusVo(message, status):
    dict = {}
    dict["message"] = message
    dict["status"] = status
    return dict


def args_verification(*args):
    for each in args:
        if each is None:
            print("Arguement ", each, " is None")
            return False
    return True


def allowed_file(filename):
    extensions = set(current_app.config['ALLOWED_EXTENSIONS'].split(','))
    return '.' in filename and filename.rsplit('.', 1)[1] in extensions
