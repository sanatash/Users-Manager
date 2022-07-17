"""
Web interface server implemented by Flask
"""

import os
import signal
import sys

from flask import Flask, request
from db_connector import *

app = Flask(__name__)

@app.route('/users/get_user_data/<user_id>')
def web_app_rest_api(user_id):
    """
    RestApi Frontend web server which implements Get method
    :param user_id: user_id variable placeholder in url
    :type user_id: int
    :return: HTML formatted string
            with user_name on success
            "no such user" error if user_id is not found in database
            "other message" error if other type of FAIL occurred
    :rtype: string
    """
    print(f"web_api_py: database user: {sys.argv[1]}, pass: {sys.argv[2]}")

    try:
        user_name = db_get_user_name(user_id)
        return "<H1 id='user'>" + user_name + "</H1>"
    except ValueError as e:
        return "<H1 id='error'>" + " no such user: " + str(user_id) + "</H1>"
    except pymysql.err.Error as e:
         return "<H1 id='error'>" + str(e) + "</H1>"

@app.route('/stop_server')
def stop_server():
    """
    Function that stops this RestAPI Web Server
    :return:  "Server stopped" in case that this succeed
            "Didn't succeed to kill the web_api server" in case that kill function didn't succeed
    :rtype:
    """
    try:
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
        return "Server stopped"
    except:
        print("Didn't succeed to kill the web_api server")

app.run(host='127.0.0.1', debug=True, port=5001)