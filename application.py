from flask import Flask, request
from flask import render_template
from users import *
import json
from database import *
from collections import namedtuple
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@application.route('/')
def hello_world():
    return 'Hello World!'


@application.route('/get_user')
def login_user():
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


@application.route('/get_city')
def fun_get_city():
    city_name = request.args['city_name']
    city = get_city(city_name)
    # return json.dumps(city, default=lambda o: o.__dict__)
    return json.dumps(city)


@application.route('/get_city_list_by_preference')
def fun_get_city_list():
    user = json.loads(request.args['user'], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    if not EMAIL_REGEX.match(user):
        return "Error: wrong format of user email"
    search_size = request.args['search_size']

    preferences = user.preferences
    city_list = search_city_by_preferences(preferences, search_size)
    # return json.dumps(city_list, default=lambda o: o.__dict__)
    return json.dumps(city_list)


@application.route('/search_job_by_skills')
def fun_get_job_list_by_skills():
    user = json.loads(request.args['user'], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    if not EMAIL_REGEX.match(user):
        return "Error: wrong format of user email"
    search_size = request.args['search_size']
    skills = get_user_from_db(email=user)['skill']
    jobs = search_job_by_skills(skills, search_size)
    # return json.dumps(jobs, default=lambda o: o.__dict__)
    return json.dumps(jobs)


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
