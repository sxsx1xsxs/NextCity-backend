
def get_user(email):
    """
    :param email:
    :return: if the user with the email exists in the database, return the user.
    Otherwise return null
    """
    from users import User
    user = User(email, "dummy")

    return user
    # return None


def store_user(user):
    """
    :param user:
    :return: True if successfully stored the user, false otherwise
    """
    return True


def get_city(city_name):
    from city import City
    city = City("Chicago")
    return city


def search_city_by_preferences(preferences, size):
    """
    :param preferences: String[]
    :return:
    """
    from job import Job
    job1 = Job("job1")
    job2 = Job("job2")
    jobs = [job1, job2]
    return jobs


def search_job_by_city(city, size):
    """
    :param cities: String[]
    :param size: int
    :return: Job[]
    """
    from job import Job
    job1 = Job("job1")
    job2 = Job("job2")
    jobs = [job1, job2]
    return jobs


def search_job_by_skills(skills, size):
    """
    :param skills: String[]
    :param size: int
    :return: Job[]
    """
    from job import Job
    job1 = Job("job1")
    job2 = Job("job2")
    jobs = [job1, job2]
    return jobs


def search_job_by_keywords(keywords, size):
    """
    :param keywords: String[]
    :param size: int
    :return: Job[]
    """
    from job import Job
    job1 = Job("job1")
    job2 = Job("job2")
    jobs = [job1, job2]
    return jobs
