"""
REST API server implemented by Flask
"""

import os
import signal
import sys

from flask import Flask, request
from db_connector import *

app = Flask(__name__)

def add_user_api(user_id):
    """
    Takes care of PUT RestApi method that adds new user to the database with next info:
        - user_id is argument to the function
        - user_name is found in JSON payload of Rest API request
    :param user_id: user_id to add
    :type user_id: int
    :return: - success if user addition succeed + code 200 (success)
             - error with reason 'id already exist' if such user id is already exist in the database + code 500 (fail)
             - error with other reason if failure user addition caused by other error + code 500 (fail)
    :rtype: JSON file + return code
    """
    try:
        request_data = request.json
        user_name = request_data.get('user_name')
        db_insert_user(user_id, user_name)
        return {'status': 'ok', 'user added': user_name}, 200

    except pymysql.err.Error as e:
        if str(e).find("Duplicate entry"):
            return {'status': 'error', 'reason': 'id already exist'}, 500
        else:
            return {'status': 'error', 'reason': {str(e)}}, 500

def get_user_name_api(user_id):
    """
    Takes care of GET RestApi method that returns the name of user found in database
    :param user_id: user_id whose name to return
    :type user_id: int
    :return: - success if get of user name succeed + code 200 (success)
             - error with reason 'no such id' if user id is not found in the database + code 500 (fail)
             - error with other reason if failure of get of user name caused by other error + code 500 (fail)
    :rtype: JSON file + return code
    """
    try:
        user_name = db_get_user_name(user_id)
        return {'status': 'ok', 'user_name': user_name}, 200
    except ValueError as e:
        return {'status': 'error', 'reason': 'no such id'}, 500
    except pymysql.err.Error  as e:
        return {'status': 'error', 'reason': str(e)}, 500

def change_user_name_api(user_id, user_name):
    """
    Takes care of PUT RestApi method that changes the name of user found in database
    :param user_id: user_id to change its user_name
    :type user_id: int
    :param user_name: new user_name that should replace old user_name
    :type user_name: string
    :return: - success if change of user name succeed + code 200 (success)
             - error with reason 'no such id' if user id is not found in the database + code 500 (fail)
             - error with other reason if failure of change of user name caused by other error + code 500 (fail)
    :rtype: JSON file + return code
    """
    try:
        request_data = request.json
        user_name = request_data.get('user_name')
        db_change_user_name(user_id, user_name)
        return {'status': 'ok', 'user_updated': user_name}, 200
    except ValueError as e:
        return {'status': 'error', 'reason': 'no such id'}, 500
    except pymysql.err.Error as e:
            return {'status': 'error', 'reason': str(e)}, 500

def delete_user_api(user_id):
    """
    Takes care of DELETE RestApi method and deleted user from database
    :param user_id: user_id of user to delete
    :type user_id: int
    :return: - success if deletion of user from the database succeed + code 200 (success)
             - error with reason 'no such id' if user id is not found in the database + code 500 (fail)
             - error with other reason if failure of user deletion caused by other error + code 500 (fail)
    :rtype: JSON file + return code
    """
    try:
        db_delete_user(user_id)
        return {'status': 'ok', 'user_deleted': user_id}, 200
    except ValueError as e:
        return {'status': 'error', 'reason': 'no such id'}, 500
    except pymysql.err.Error as e:
        return {'status': 'error', 'reason': str(e)}, 500

@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def users_rest_api(user_id):
    """
    RestApi Backend server which implements Get/POST/PUT/DELETE methods
    :param user_id: user_id variable placeholder in url
    :type user_id: int
    :return: JSON file + return code
    :rtype: JSON file + int
    """
    db_save_credentials(sys.argv[1], sys.argv[2])

    if request.method == 'POST':
        return add_user_api(user_id)
    elif request.method == 'GET':
        return get_user_name_api(user_id)
    elif request.method == 'PUT':
        return change_user_name_api(user_id)
    elif request.method == 'DELETE':
        return delete_user_api(user_id)

@app.route('/stop_server')
def stop_server():
    """
    Function that stops this rest_api Server
    :return:  "Server stopped" in case that this succeed
            "Didn't succeed to kill the rest_api server" in case that kill function didn't succeed
    :rtype:  string
    """
    try:
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
        return "Server stopped"
    except:
        print("Didn't succeed to kill the rest_api server")

app.run(host='127.0.0.1', debug=True, port=5000)