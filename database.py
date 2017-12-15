from users import *


class Database:
    @staticmethod
    def get_user(email):
        return User(email, "dummy_name")

    @staticmethod
    def store_user(user):
        # store the user information into the database
        return True
