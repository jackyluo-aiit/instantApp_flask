from flask import Flask
from instantApp.extensions import db, mail, login_manager, socketio
from instantApp.messages import messages_bp
from instantApp.auth import auth_bp
from instantApp.chats import chats_bp
from instantApp.settings import config

print('initiating')


def create_app(config_name='development'):
    app = Flask('instantApp')
    app.config.from_object(config[config_name])
    app.register_blueprint(messages_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    register_extensions(app)

    @login_manager.user_loader
    def load_user(user_id):
        from instantApp.models import User
        user = User.query.get(int(user_id))
        return user

    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
