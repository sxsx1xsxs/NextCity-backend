import pymysql
import json


def db_conn():  # ZJ
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


def db_conqyy():  # QYY
    return pymysql.connect(host="cc-nextcity.c3roxefgeyor.us-west-2.rds.amazonaws.com",
                           port=3306,
                           user="root",
                           passwd="rootroot",
                           db="nextcity",
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor,
                           )


def get_user_except(email, size=100):
    db = db_conqyy()
    cursor = db.cursor()
    sql = "select * from user where email != %s"
    try:
        cursor.execute(sql, email)
        users = cursor.fetchall()
        db.close()
        return users[:size]
    except:
        print("Error: unable to fetch data")
        db.close()


def get_user_from_db(email):  # YKM
    """
    :param email:
    :return: if the user with the email exists in the database, return the user.
    Otherwise return null
    """
    db = db_conqyy()
    # cursor = db.cursor()
    # sql = "select * from user where email = %s"
    cursor = db.cursor()
    sql = "select * from user where email = %s"
    try:
        cursor.execute(sql, email)
        user = cursor.fetchall()[0]
        for field in ["skill", "other_pref", "main_pref"]:
            if field in user and user[field] != None:
                tmp = list(user[field].strip().split(','))
                user[field] = list(map(lambda x: x.strip(), tmp))
        db.close()
        return user
    except:
        print("Error: unable to fetch data")
        db.close()


def store_user(user):  # QYY

    """
    :param user:
    :return: True if successfully stored the user, false otherwise
    """

    # user is a dict mapping name, skill, main_pref, other_pref, email, password
    db = db_conn()
    cursor = db.cursor()

    properties = ('name', 'skill', 'main_pref', 'other_pref', 'email', 'password', 'address')
    sql = "insert into user (" + ",".join(properties) + ") VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for property in properties:
        user[property] = None if not property in user else user[property]

    try:
        cursor.execute(sql, (
            user["name"], user["skill"], user["main_pref"], user["other_pref"], user["email"], user["password"],
            user["address"]))
        db.commit()
        db.close()
        return True
    except:
        print("Error: unable to store data")
        db.close()
        return False

def update_user(user): # ZJ
    """
    :param user:
    :return: user if successfully update the user, None otherwise
    """
    if (not 'email' in user) or (user['email'] == None) or (get_user_from_db(user['email']) == None):
        return None

    db = db_conn()
    cursor = db.cursor()

    properties = ('name', 'skill', 'main_pref', 'other_pref', 'email', 'password', 'address')
    sql = "update user set name = %s, skill = %s, main_pref = %s, other_pref = %s, password = %s, address = %s " \
          "WHERE email = %s"

    for property in properties:
        user[property] = None if not property in user else user[property]

    try:
        cursor.execute(sql, (
            user["name"], user["skill"], user["main_pref"], user["other_pref"], user["password"],
            user["address"], user["email"]))
        db.commit()
        db.close()
        return user
    except:
        print("Error: unable to update data")
        db.close()
        return None


def get_city(city_name):  # ZJ
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
        db.close()
        return city
    except:
        print('Error: unable to fetch data')
        db.close()


def search_city_by_preferences(preferences, size):
    """
    :param preferences: String[]
    :param size: int
    :return: [dict]
    """
    result = []
    db = db_conqyy()
    cursor = db.cursor()
    sql = "select * from city order by %s"
    try:
        cursor.execute(sql, ','.join(preferences))
        cities = cursor.fetchall()
        for city in cities:
            result.append(city)
        db.close()
        return result[:size]
    except:
        db.close()
        print("Error: unable to fetch data")


def get_all_jobs(size=100):
    result = []
    db = db_conqyy()
    cursor = db.cursor()
    sql = "select * from job"
    try:
        cursor.execute(sql)
        jobs = cursor.fetchall()
        for job in jobs:
            result.append(job)
        db.close()
        return result[:size]
    except:
        db.close()
        print("Error: unable to fetch data")


def search_job_by_city(city_name, size=100):  # QYY
    """
    :param city_name: String
    :param size: int
    :return: [dict]
    """
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
        db.close()
        print("Error: unable to fetch data")


def search_job_by_skills(skills, size=100):
    """
    :param skills: String[]
    :param size: int
    :return: [dict]
    """
    result = []
    db = db_conqyy()
    cursor = db.cursor()
    sql = "select * from job where skill LIKE (%s)"
    for skill in skills:
        try:
            cursor.execute(sql, skill)
            jobs = cursor.fetchall()
            for job in jobs:
                result.append(job)
        except:
            print("Error: unable to fetch data")
            db.close()
    db.close()
    return result[:size]


def search_job_by_keywords(keywords, size=100):  # ZJ
    """
    :param keywords: String[]
    :param size: int
    :return: [dict]
    """
    result = []
    db = db_conqyy()
    cursor = db.cursor()
    sql = "select * from job WHERE match(title, city, company, state, skill, description) against (%s in BOOLEAN MODE )"
    keyword_boolean = ""
    for keyword in keywords:
        keyword_boolean += '+' + keyword + ' '
    try:
        cursor.execute(sql, keyword_boolean)
        jobs = cursor.fetchall()
        for job in jobs:
            result.append(job)
        db.close()
        return result[:size]
    except:
        db.close()
        print("Error: unable to fetch data")


def store_userfavorjob(email, jobid):  # QYY
    """
    :param email: String
    :param jobid: int
    :return: Ture if succesful; False if failed
    """
    db = db_conqyy()
    cursor = db.cursor()
    sql = "insert into userfavorjob (email, jobid) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (email, jobid))
        db.commit()
        db.close()
        return True
    except:
        db.close()
        print("Error: unable to store data")
        return False


def get_userfavorjobs(email):  # QYY
    """
    :param email: String
    :return: a list of job maps of this user
    1. get the all the uer's favored jobid   put all jobids in a list
    2. use the for loop to iterate the jobids list and find all corresponding jobs and put results in one list
    """
    db = db_conqyy()
    cursor = db.cursor()
    sql1 = "select jobid from userfavorjob where email = (%s)"
    sql2 = "select * from job where id = (%s)"
    try:
        cursor.execute(sql1, email)
        jobids = cursor.fetchall()
        print(jobids)
        jobidslist = []
        for jobidmap in jobids:
            jobid = jobidmap["jobid"]
            print(jobid)
            jobidslist.append(jobid)
        print(jobidslist)
        result = []
        for jobid in jobidslist:
            cursor.execute(sql2, jobid)
            rows = cursor.fetchall()
            result.append(rows[0])
        db.close()
        return result
    except:
        print("unable to fetch data")
        db.close()


# Test
def main():
    # store_user({'email' : 'zhijian.jiang@foxmail.com'})
    print(update_user({'email' : 'zhijian.jiang@gmail.com', 'skill' : 'C++'}))


if __name__ == '__main__':
    main()
