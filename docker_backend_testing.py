"""
Module which performs testing of backend side running inside the docker (dockerized rest_api module)
"""
import sys

import requests
from db_docker_connector import db_get_user_name
from db_docker_connector import db_get_all_tests_config, db_get_max_user_id

def docker_backend_server_test(user_id, user_name):
    """
    Testing the rest_api backend server by posting new user and checking that it's name is correct by GET request and selecting data from the database
    :param user_id: user_id to POST
    :type user_id: int
    :param user_name: user_name
    :type user_name: string
    """
    host = "rest_api"
    port = 5000
    url = f"http://{host}:{port}/users/{user_id}"
    payload = {"user_name": user_name}
    # Step 1
    post_response = requests.post(url, json=payload)
    # Step 2
    get_response = requests.get(url)
    if get_response.json()['status'] == 'ok':
        if get_response.json()['user_name'] != user_name or get_response.status_code != 200:
            raise Exception("docker backend test failed")
    elif get_response.json()['status'] == 'error':
        raise Exception("docker backend test failed")

    # Step 3
    db_name = db_get_user_name(user_id)
    if db_name != user_name:
        raise Exception("docker backend test failed")

if __name__ == '__main__':
    try:
        all_tests = db_get_all_tests_config()

        for test in all_tests:
            max_user_id = db_get_max_user_id()
            user_name_to_insert = test[3]
            docker_backend_server_test(max_user_id+1, user_name_to_insert)

    except:
        raise Exception("docker backend test failed")
