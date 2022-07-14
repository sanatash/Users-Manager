"""
File for combined testing of rest_api (backend) and web_api (frontend) sides
"""
import frontend_testing
import backend_testing
from db_connector import db_get_all_tests_config, db_get_max_user_id

def combined_testing_suite():
    """
    Performs combined testing of both frontend and backend Flask servers.
    Receives all tests from config table and runs it row after row.
    For every user that should be added, finds what is max user_id existing and
    adds next user with max+1 user_id
    """
    try:
        all_tests = db_get_all_tests_config()

        for test in all_tests:
            max_user_id = db_get_max_user_id()

            user_name_to_insert = test[3]
            backend_testing.backend_server_test(max_user_id+1, user_name_to_insert)

            api_gateway_url = test[1]
            browser_name = test[2]
            frontend_testing.web_test(max_user_id+1, user_name_to_insert, api_gateway_url, browser_name)
    except:
        raise Exception("test failed")

if __name__ == '__main__':
    try:
        combined_testing_suite()
    except:
        raise Exception("combined test failed")