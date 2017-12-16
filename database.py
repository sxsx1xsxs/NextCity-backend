
def get_user_from_db(email): # Yiyang
    """
    :param email:
    :return: if the user with the email exists in the database, return the user.
    Otherwise return null
    """
    # from users import User
    # user = User(email, "dummy")
    user = {}
    return user
    # return None


def store_user(user): # Yiyang
    """
    :param user:
    :return: True if successfully stored the user, false otherwise
    """
    return True


def get_city(city_name): # Yiyang
    # from city import City
    # city = City("Chicago")
    city = {}
    return city


def search_city_by_preferences(preferences, size): # Yiyang
    """
    :param preferences: String[]
    :param size: int
    :return: [dict]
    """
    city1 = {}
    city2 = {}

    city1['name'] = 'name' # modify this line
    # from job import Job
    # city1 = Job("city1")
    # city2 = Job("city2")
    # cities = [city1, city2]

    return [city1, city2]


def search_job_by_city(city_name, size):
    """
    :param city_name: String
    :param size: int
    :return: [dict]
    """
    # from job import Job
    # job1 = Job("job1")
    # job2 = Job("job2")
    # jobs = [job1, job2]
    job1 = {}
    job2 = {}

    job1['name'] = 'name' # modify this line
    return [job1, job2]


def search_job_by_skills(skills, size):
    """
    :param skills: String[]
    :param size: int
    :return: [dict]
    """
    job1 = {}
    job2 = {}

    job1['name'] = 'name'  # modify this line
    return [job1, job2]


def search_job_by_keywords(keywords, size):
    """
    :param keywords: String[]
    :param size: int
    :return: [dict]
    """
    job1 = {}
    job2 = {}

    job1['name'] = 'name'  # modify this line
    return [job1, job2]
