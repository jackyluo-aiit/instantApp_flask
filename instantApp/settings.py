import os


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-emails'


class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY', 'default')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ("instantApp", MAIL_USERNAME)

    WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    SENDFILE_URL = os.getenv("SENDFILE_URL")
    ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEVELOPMENT_SQLALCHEMY_DATABASE_URI')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_SQLALCHEMY_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
