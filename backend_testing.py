"""
Module which performs testing of backend side (rest_api module)
"""

import requests
from db_connector import db_get_user_name

def backend_server_test(user_id, user_name):
    """
    Testing the rest_api backend server by posting new user and checking that it's name is correct by GET request and selecting data from the database
    :param user_id: user_id to POST
    :type user_id: int
    :param user_name: user_name
    :type user_name: string
    """

    url = f"http://127.0.0.1:5000/users/{user_id}"
    payload = {"user_name": user_name}

    # Step 1
    post_response = requests.post(url, json=payload)
    # Step 2
    get_response = requests.get(url)

    if get_response.json()['status'] == 'ok':
        if get_response.json()['user_name'] != user_name or get_response.status_code != 200:
            raise Exception("backend test failed")
    elif get_response.json()['status'] == 'error':
        raise Exception("backend test failed")

    # Step 3
    db_name = db_get_user_name(user_id)
    if db_name != user_name:
        raise Exception("backend test failed")
