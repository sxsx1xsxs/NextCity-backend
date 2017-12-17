import pymysql
import json

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


def get_user_except(email, size=100):
    db = db_conqyy()
    cursor = db.cursor()
    sql = "select * from user where email != %s"
    try:
        cursor.execute(sql, email)
        jobs = cursor.fetchall()
        db.close()
        return jobs[:size]
    except:
        print("Error: unable to fetch data")
        db.close()

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
        db.close()
        return user
    except:
        db.close()
        print('Error: unable to fetch data')

def store_user(user): # QYY

    """
    :param user:
    :return: True if successfully stored the user, false otherwise
    """

    # user is a dict mapping name, skill, main_pref, other_pref, email, password
    db = db_conn()
    cursor = db.cursor()
    sql = "insert into user (name, skill, main_pref, other_pref, email, password, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    user['name'] = None if not 'name' in user else user['name']
    user['skill'] = None if not 'skill' in user else user['skill']
    user['main_pref'] = None if not 'main_pref' in user else user['main_pref']
    user['other_pref'] = None if not 'other_pref' in user else user['other_pref']
    user['email'] = None if not 'email' in user else user['email']
    user['password'] = None if not 'password' in user else user['password']
    user['address'] = None if not 'address' in user else user['address']

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



def search_job_by_city(city_name, size = 100): #QYY
    """
    :param city_name: String
    :param size: int
    :return: [dict]
    """
    # from job import Job
    # job1 = Job("job1")
    # job2 = Job("job2")
    # jobs = [job1, job2]
    # size = 100
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


def search_job_by_keywords(keywords, size=100): #ZJ
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

# Test
def main():
    store_user({'email' : 'zhijian.jiang@foxmail.com'})
    print(get_user_from_db('Yerbury.Edouard@gmail.com'))

if __name__ == '__main__':
    main()
    # print(get_user_from_db("Alonzo.Ball@gmail.com"))

    # user = {"name": "qyy", "skill": "a,b,c", "main_pref": "e,g,h", "other_pref": "sf,d", "email": "KLJF", "password": "safe", "address": "203"}
    # print(store_user(user))


