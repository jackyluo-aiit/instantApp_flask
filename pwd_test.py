from werkzeug.security import generate_password_hash, check_password_hash


class User():
    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.pwd_hash, password)


user = User()
user.set_password('cat')
print(user.validate_password('cat'))
