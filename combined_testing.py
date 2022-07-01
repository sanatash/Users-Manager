import frontend_testing
import backend_testing


def combined_testing_suite(user_id, user_name):
    try:
        backend_testing.backend_server_test(user_id, user_name)
        frontend_testing.web_test(user_id, user_name)
    except:
        raise Exception("test failed")

user_id = 15
user_name = "Dorian"
combined_testing_suite(user_id, user_name)