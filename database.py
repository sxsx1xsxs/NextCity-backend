import pymysql


def db_conn():
    return pymysql.connect(host="cc-nextcity.c3roxefgeyor.us-west-2.rds.amazonaws.com",
                         port=3306,
                         user="root",
                         passwd="rootroot",
                         db="nextcity")

def get_fields_name(cursor):
    """
    :param: cursor
    :return: list of fields name
    """
    return [i[0] for i in cursor.description]


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
    db = db_conn()
    cursor = db.cursor()
    sql = "select * from city where city_name = %s"
    city = {}
    try:
        cursor.execute(sql, (city_name))
        fields_name = get_fields_name(cursor)
        results = cursor.fetchall()
        row = results[0]
        for i in range(len(row)):
            city[fields_name[i]] = row[i]
        # for row in results:
        #
    except:
        print('Error: unable to fetch data')

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

# Test
def main():
    get_city('New York')
    
if __name__ == '__main__':
    main()
