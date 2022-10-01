"""
Module which performs testing of backend side running inside the docker (dockerized rest_api module)
"""
import sys

import requests
from urllib.parse import urlparse

def read_host_and_port():
    with open('k8s_url.txt', 'r') as file:
        line = file.readline()
        parsed = urlparse(line)

    return (parsed.hostname, parsed.port)

def docker_backend_server_test(user_id, user_name):
    """
    Testing the rest_api backend server by posting new user and checking that it's name is correct by GET request and selecting data from the database
    :param user_id: user_id to POST
    :type user_id: int
    :param user_name: user_name
    :type user_name: string
    """

    host, port = read_host_and_port()
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

def backend_get_all_tests_config():
    """
    Brings all tests from config table through the rest_api service
    """
    host, port = read_host_and_port()
    url = f"http://{host}:{port}/config"

    get_response = requests.get(url)
    if get_response.json()['status'] == 'ok':
        if get_response.status_code != 200:
            raise Exception("docker backend test failed")
    elif get_response.json()['status'] == 'error':
        raise Exception("docker backend test failed")

    return get_response.json()['all tests']

def backend_get_max_user_id():
    """
    Ask what the maximum users id in users table through the rest_api service
    """
    # host = "restapi"
    # port = 5000
    host, port = read_host_and_port()
    url = f"http://{host}:{port}/get_max_id"

    get_response = requests.get(url)
    if get_response.json()['max_id'] == 'ok':
        if get_response.status_code != 200:
            raise Exception("docker backend test failed")
    elif get_response.json()['status'] == 'error':
        raise Exception("docker backend test failed")

    return get_response.json()['max_id']


if __name__ == '__main__':
    try:
        all_tests = backend_get_all_tests_config()

        for test in all_tests:
            max_user_id = backend_get_max_user_id()
            print(max_user_id)
            user_name_to_insert = test[3]
            print(user_name_to_insert)
            docker_backend_server_test(max_user_id+1, user_name_to_insert)

    except:
        raise Exception("docker backend test failed")
