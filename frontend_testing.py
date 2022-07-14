"""
Module which performs testing of Web interface (web_api module)
"""

import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from db_connector import db_get_all_tests_config, db_get_user_name

def web_test(user_id, user_name, api_gateway_url, browser_name):
    """
    Testing the web_app RestApi server by Selenium:
        - checks that user_id exist and it's name is correct
    :param user_id: user_id to check
    :type user_id: int
    :param user_name: the correct user_name for given user_id
    :type user_name: string
    :param api_gateway_url: api_gateway_url where web frontend server is running
    :type api_gateway_url: url string
    :param browser_name: the browser where api_gateway_url should be opened
    :type browser_name: string
    """
    try:
        if browser_name.lower() == "chrome":
            driver = webdriver.Chrome(executable_path="D:/Anat/chromedriver_win32/ChromeDriver.exe")
        elif browser_name.lower() == "firefox":
            driver = webdriver.Firefox(executable_path="D:/Anat/firefoxdriver_win64/geckodriver.exe")
        else:
            driver = webdriver.Chrome(executable_path="D:/Anat/chromedriver_win32/ChromeDriver.exe")

        driver.get(f"{api_gateway_url}/{user_id}")
        time.sleep(2)

        user_element = driver.find_element(by=By.ID, value="user")
        if not user_element.is_displayed():
            raise Exception(Exception("frontend test failed"))
        if user_element.text != user_name:
            raise Exception(Exception("frontend test failed"))

        print(f"web_test: for user_id={user_id}, the user_name=", user_element.text)

        driver.quit()
    except pymysql.err.Error as e:
        print(e)
        raise Exception(Exception("frontend test failed"))
    except:
        raise Exception(Exception("frontend test failed"))

if __name__ == '__main__':
    try:
        all_tests = db_get_all_tests_config()

        for test in all_tests:
            user_id = test[0]
            user_name_to_check = db_get_user_name(user_id)
            api_gateway_url = test[1]
            browser_name = test[2]
            web_test(user_id, user_name_to_check, api_gateway_url, browser_name)
    except:
        raise Exception("frontend test failed")