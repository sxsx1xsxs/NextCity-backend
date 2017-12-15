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

    def get_total_similarity(a, b):
        key = "name"
        compare1 = "skill"
        compare2 = "pref"

        res = {}
        for item in b:
            cnt = 0
            for v in a[compare1]:
                if v in item[compare1]:
                    cnt += 1
            res[item[key]] = cnt / len(a[compare1]) / 2

        for item in b:
            cnt = 0
            for i in range(len(a[compare2])):
                if a[compare2][i] in item[compare2]:
                    cnt += abs(i - item[compare2].index(a[compare2][i]))
                else:
                    cnt += len(a[compare2])
            res[item[key]] += (1 - cnt / (len(a[compare2]) * len(a[compare2]))) / 2

        return sorted(res.items(), key=lambda x: x[1], reverse=True)
