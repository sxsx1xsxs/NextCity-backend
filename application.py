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
    user = get_user_from_db(email)
    return json.dumps(user)


@application.route('/save_user', methods=['POST'])
def save_user():
    user = json.loads(request.args['user'], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    store_user(user)
    return "success saving " + request.args['user']


@application.route('/update_user', methods=['POST'])
def fun_update_user():
    # check valid

    user = request.get_json()
    if not 'email' in user:
        print('Error: email is absent')
        return json.dumps(False)
    email = user['email']
    if not EMAIL_REGEX.match(email):
        print("Error: wrong format of user email")
        return json.dumps(False)

    # join preference
    prefs = ('main_pref', 'other_pref', 'skill')
    for pref in prefs:
        if pref in user and user[pref] != None:
            user[pref] = ','.join(user[pref])

    return json.dumps(update_user(user))


@application.route('/signup_user', methods=['POST'])
def fun_signup_user():
    # check email and password
    if not ('email' in request.form and 'password' in request.form):
        print("Error: empty email or password")
        return json.dumps(False)
    email = request.form['email']
    if not EMAIL_REGEX.match(email):
        print("Error: wrong format of user email")
        return json.dumps(False)
    if get_user_from_db(email) != None:
        print('Error: this email exists')
        return json.dumps(False)

    password = request.form['password']
    name = request.form['name'] if 'name' in request.form else None
    try:
        store_user({'email': email, 'password': password, 'name': name})
        return json.dumps(True)
    except:
        return json.dumps(False)


@application.route('/login_user', methods=['POST'])
def fun_login_user():
    email = request.form['email']
    if not EMAIL_REGEX.match(email):
        return "Error: wrong format of user email"
    password = request.form['password']
    user = get_user_from_db(email)
    if user == None or password != user['password']:
        return json.dumps(False)
    else:
        return json.dumps(user)


@application.route('/get_city')
def fun_get_city():
    city_name = request.args['city_name']
    city = get_city(city_name)
    return json.dumps(city)


'''
sample url: http://127.0.0.1:5000/get_city_list_by_preference?email=Alonzo.Ball@gmail.com&list_size=100
sample output: ["Oakland", "New York", "Honolulu", "Berkeley", "Queens", "San Francisco", "San Francisco", "Los Angeles", "New York" ...]
there are duplicated in output
'''


@application.route('/get_city_list_by_preference')
def fun_get_city_list():
    email = request.args['email']
    if not EMAIL_REGEX.match(email):
        return "Error: wrong format of user email"
    list_size = request.args['list_size']

    user = get_user_from_db(email)
    other_users = get_user_except(email=email)
    import logic
    other_users = logic.get_total_similarity(user, other_users)
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
    return json.dumps(get_all_jobs())


@application.route('/search_job_by_kw')
def fun_get_job_by_kw():
    kw = request.args.get('kw').split(' ')
    size = 100
    jobs = search_job_by_keywords(kw, size)
    return json.dumps(jobs)


@application.route('/search_job_by_city')
def fun_get_job_list_by_city():
    city_name = request.args['city_name']
    search_size = 100
    jobs = search_job_by_city(city_name, search_size)
    return json.dumps(jobs)


@application.route('/get_favorite_job')
def fun_get_favorite_job():
    email = request.args['email']
    return json.dumps(get_userfavorjobs(email))


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    # application.run(host='0.0.0.0', port=8111)
    application.run(host='localhost', port=8111)
