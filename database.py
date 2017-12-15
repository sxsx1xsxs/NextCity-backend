
def get_user(email):
    from users import User
    user = User(email, "dummy")
    return user

    # @staticmethod
    # def store_user(user):
    #     # store the user information into the database
    #     return True
