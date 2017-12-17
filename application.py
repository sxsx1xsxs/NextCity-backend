from flask import Flask, request
from flask import render_template
from users import *
import json
from database import *
from collections import namedtuple, Set
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@application.route('/')
def hello_world():
    return 'Hello World!'


@application.route('/get_user')
def fun_get_user():
    email = request.args['email']
    name = request.args['name']
    user = get_user_from_db(email)

    if len(user) == 0:
        user['email'] = email
        user['name'] = name
        store_user(user)
    return json.dumps(user)

@application.route('/save_user', methods=['POST'])
def save_user():
    user = json.loads(request.args['user'], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    store_user(user)
    # print(user.name)
    return "success saving " + request.args['user']

@application.route('/login_user', methods=['POST'])
def fun_login_user():
    email = request.form['email']
    if not EMAIL_REGEX.match(email):
        return "Error: wrong format of user email"
    password = request.form['password']
    if password == get_user_from_db(email)['password']:
        return json.dumps(True)
    else:
        return json.dumps(False)

@application.route('/get_city')
def fun_get_city():
    city_name = request.args['city_name']
    city = get_city(city_name)
    # return json.dumps(city, default=lambda o: o.__dict__)
    return json.dumps(city)


'''
sample url: http://127.0.0.1:5000/get_city_list_by_preference?email=Alonzo.Ball@gmail.com&list_size=100
sample output: ["Oakland", "New York", "Honolulu", "Berkeley", "Queens", "San Francisco", "San Francisco", "Los Angeles", "New York" ...]
there are duplicated in output
'''


@application.route('/get_city_list_by_preference')
def fun_get_city_list():
    # user = json.loads(request.args['user'], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    email = request.args['email']
    # print(user)
    if not EMAIL_REGEX.match(email):
        return "Error: wrong format of user email"
    list_size = request.args['list_size']

    user = get_user_from_db(email)
    other_users = get_user_except(email=email)
    import logic
    other_users = logic.get_total_similarity(user, other_users)
    # city_list = search_city_by_preferences(preferences, search_size)
    # return json.dumps(city_list, default=lambda o: o.__dict__)
    cities = [other_user['address'] for other_user in other_users]
    res = []
    seen = set([])
    cnt = 0
    for city in cities:
        if cnt == int(list_size):
            break
        if city not in seen:
            seen.add(city)
            res.append(city)
            cnt += 1

    return json.dumps(res)


@application.route('/get_all_jobs')
def fun_get_all_jobs():
    # size = json.loads(request.args['size'], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    # jobs = get_all_jobs(size=size) if not size is None else get_all_jobs()
    return json.dumps(get_all_jobs())


# @application.route('/search_job_by_skills')
# def fun_get_job_list_by_skills():
#     user = json.loads(request.args['user'], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
#     if not EMAIL_REGEX.match(user):
#         return "Error: wrong format of user email"
#     search_size = request.args['search_size']
#     skills = get_user_from_db(email=user)['skill']
#     jobs = search_job_by_skills(skills, search_size)
#     # return json.dumps(jobs, default=lambda o: o.__dict__)
#     return json.dumps(jobs)


@application.route('/search_job_by_kw')
def fun_get_job_by_kw():
    kw = request.args.get('kw').split(' ')
    size = 100
    print(kw)
    jobs = search_job_by_keywords(kw, size)
    return json.dumps(jobs)


@application.route('/search_job_by_city')
def fun_get_job_list_by_city():
    city_name = request.args['city_name']
    search_size = 100
    jobs = search_job_by_city(city_name, search_size)
    return json.dumps(jobs)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
