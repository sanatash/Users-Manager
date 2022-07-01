"""
Module which performs testing of Web interface (web_api module)
"""

import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By

def web_test(user_id, user_name):
    """
    Testing the web_app RestApi server by Selenium:
        - checks that user_id exist and it's name is correct
    :param user_id: user_id to check
    :type user_id: int
    :param user_name: the correct user_name
    :type user_name: string
    """
    try:
        driver = webdriver.Chrome(executable_path="D:/Anat/chromedriver_win32/ChromeDriver.exe")

        driver.get(f"http://127.0.0.1:5001//users/get_user_data/{user_id}")
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
