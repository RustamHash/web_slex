from flask_login import UserMixin

class UserLogin(UserMixin):
    def from_db(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_login(self):
        return str(self.__user['login'])

    def get_username(self):
        return str(self.__user['username'])

    def get_id(self):
        return str(self.__user['id'])