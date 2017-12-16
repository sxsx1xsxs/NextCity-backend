import pymysql


def db_conn(): #ZJ
    return pymysql.connect(host="cc-nextcity.c3roxefgeyor.us-west-2.rds.amazonaws.com",
                         port=3306,
                         user="root",
                         passwd="rootroot",
                         db="nextcity",
                           )

def get_fields_name(cursor):
    """
    :param: cursor
    :return: list of fields name
    """
    return [i[0] for i in cursor.description]

def db_conqyy(): #QYY
    return pymysql.connect(host="cc-nextcity.c3roxefgeyor.us-west-2.rds.amazonaws.com",
                           port=3306,
                           user="root",
                           passwd="rootroot",
                           db="nextcity",
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor,
                           )


# def get_user_from_db(email): # QYY
#     """
#     :param email:
#     :return: if the user with the email exists in the database, return the user.
#     Otherwise return null
#     """
#     # from users import User
#     # user = User(email, "dummy")
#     db = db_conqyy()
#     cursor = db.cursor()
#     sql = "select * from user WHERE email = (%s)"
#     user = {}
#     try:
#         cursor.execute(sql, email)
#         # users is a list of dicts
#         users = cursor.fetchall()
#         user = users[0]
#     except:
#         print("Error: unable to fetch data")
#
#     return user
    # return None

def get_user_from_db(email):  # YKM
    """
    :param email:
    :return: if the user with the email exists in the database, return the user.
    Otherwise return null
    """
    db = db_conn()
    cursor = db.cursor()
    sql = "select * from user where email = %s"
    user = {}
    try:
        cursor.execute(sql, email)
        fields_name = get_fields_name(cursor)
        results = cursor.fetchall()
        row = results[0]
        for i in range(len(row)):
            user[fields_name[i]] = row[i]
        for field in ["skill", "other_pref", "main_pref"]:
            tmp = list(user[field].strip().split(','))
            user[field] = list(map(lambda x: x.strip(), tmp))
    except:
        print('Error: unable to fetch data')
    db.close()
    return user


def store_user(user): # QYY
    """
    :param user:
    :return: True if successfully stored the user, false otherwise
    """
    # user is a dict mapping name, skill, main_pref, other_pref, email, password
    db = db_conqyy()
    cursor = db.cursor()
    sql = "insert into user (name, skill, main_pref, other_pref, email, password, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (user["name"], user["skill"], user["main_pref"], user["other_pref"], user["email"], user["password"], user["address"]))
        db.commit()
        db.close()
        return True
    except:
        print("Error: unable to store data")
    db.close()
    return False

def get_city(city_name): # ZJ
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
            city[fields_name[i]] = row[i] if not row[i] == None else 0
        # for row in results:
        #
    except:
        print('Error: unable to fetch data')
    db.close()
    return city


def search_city_by_preferences(preferences, size):
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


def search_job_by_city(city_name, size): #QYY
    """
    :param city_name: String
    :param size: int
    :return: [dict]
    """
    # from job import Job
    # job1 = Job("job1")
    # job2 = Job("job2")
    # jobs = [job1, job2]
    size = 100
    result = []
    db = db_conqyy()
    cursor = db.cursor()
    sql = "select * from job where city = (%s)"
    try:
        cursor.execute(sql, city_name)
        jobs = cursor.fetchall()
        for job in jobs:
            result.append(job)
        db.close()
        return result
    except:
        print("Error: unable to fetch data")
        db.close()




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


def search_job_by_keywords(keywords, size): #QYY
    """
    :param keywords: String[]
    :param size: int
    :return: [dict]
    """
    job1 = {}
    job2 = {}
    # sql = "select * from job where title like "
    for keyword in keywords:
        sql = sql + ""

    job1['name'] = 'name'  # modify this line
    return [job1, job2]

# Test
def main():
    get_city('Akron')
    
if __name__ == '__main__':
    # main()
    # print(get_user_from_db("Alonzo.Ball@gmail.com"))

    # user = {"name": "qyy", "skill": "a,b,c", "main_pref": "e,g,h", "other_pref": "sf,d", "email": "KLJF", "password": "safe", "address": "203"}
    # print(store_user(user))

    print(search_job_by_city("Dallas", 100))
