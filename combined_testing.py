"""
File for combined testing of rest_api (backend) and web_api (frontend) sides
"""
import frontend_testing
import backend_testing


def combined_testing_suite(user_id, user_name):
    """
    Performs combined testing of both frontend and backend Flask servers
    :param user_id: user_id to add
    :type user_id: int
    :param user_name: user_name
    :type user_name: string
    """
    try:
        backend_testing.backend_server_test(user_id, user_name)
        frontend_testing.web_test(user_id, user_name)
    except:
        raise Exception("test failed")

user_id = 22
user_name = "Robert"
combined_testing_suite(user_id, user_name)