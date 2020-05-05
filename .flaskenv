FLASK_APP=instantApp
FLASK_ENV=development

PRODUCTION_SQLALCHEMY_DATABASE_URI = "mysql+pymysql://lxq:123456@3.91.157.112:3306/iems5722"
DEVELOPMENT_SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:JK970227456gjk@localhost:3306/iems5722"

MAIL_SERVER = "smtp.qq.com"
MAIL_PASSWORD = "bjelyxweoubeidaf"
MAIL_USERNAME = "1576123082@qq.com"

WEBSOCKET_URL = "http://localhost:8001/api/a4/broadcast_room"

UPLOAD_FOLDER = "uploads"
SENDFILE_URL = "http://localhost:8001/send_file"
ALLOWED_EXTENSIONS = "txt,pdf,png,jpg"
