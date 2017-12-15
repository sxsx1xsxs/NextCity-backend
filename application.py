from flask import Flask, request
from flask import render_template
from users import *
import json
from database import *

application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello World!'


@application.route('/login')
def login():
    email = request.args['email']
    user = get_user(email)
    return json.dumps(user, default=lambda o: o.__dict__)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

