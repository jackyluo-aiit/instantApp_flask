from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
socketio = SocketIO()