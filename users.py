from database import *


class User:
    def __init__(self, email, name):
        self.email = email
        self.name = name
        self.skills = ["s1"]
        self.preferences = ["p1", "p2"]
        self.favoriteJobs = ["f1"]
        self.favoriteCities = ["fc1"]

    # def set_preference(self, preferences):
    #     """
    #     :param preferences: String[]
    #     """
    #     self.preferences = preferences
    #     store_user(self)
    #
    # def set_skills(self, skills):
    #     """
    #     :param skills: String[]
    #     """
    #     self.skills = skills
    #     store_user(self)
