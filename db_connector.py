"""
Database module which connect to MySQL database and performs various SQL operations
"""

from datetime import datetime
import pymysql
import mysql.connector

users_table_name = "users2"
config_table_name = "config3"

def db_connect_open():
    """
    Opens connection to the MySql database
    :return: connection object
    :rtype: Connector class
    """
    try:
        # Establishing a connection to DB
        conn = mysql.connector.connect(host= 'remotemysql.com', port=3306, user='JLHNSONLhK',
                                       passwd='HE6DJPd5an' , database='JLHNSONLhK')
        return conn

    except pymysql.err.Error as e:
        raise e


def db_connect_close(conn, cursor):
    """
    Closes connection to the database and cursor object
    :param conn: connection to database
    :type conn: Connector class
    :param cursor: cursor to the database
    :type cursor: Cursor class
    """
    cursor.close()
    conn.close()


def db_insert_user(id, name):
    """
    Inserts user into users table
    :param id:  user_id field
    :type id: int
    :param name: user_name field
    :type name: string
    """
    # connect to database
    conn = db_connect_open()
    cursor = conn.cursor(prepared=True)

    try:
        # Current date time in local system
        # creation_date = datetime.now().replace(microsecond=0)
        # Parameterized query
        sql_insert_query = f"""INSERT into JLHNSONLhK.{users_table_name} (user_id, user_name)
                            VALUES (%s, %s)"""
        # tuple to insert at placeholder
        tuple = (id, name)
        cursor.execute(sql_insert_query, tuple)
        conn.commit()

    except pymysql.err.Error as e:
        raise e

    finally:
        db_connect_close(conn, cursor)


def db_get_user_name(id):
    """
    Returns the user name stored in the database for a given user id.
    :param id: user_id
    :type id: int
    """
    # connect to database
    conn = db_connect_open()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT user_name from JLHNSONLhK.{users_table_name} WHERE user_id = {id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        return row[0]
    except pymysql.err.Error as e:
        raise e

    finally:
        db_connect_close(conn, cursor)

def db_change_user_name(id, name):
    """
    Changes user name accordingly to user id in database
    :param id: user_id
    :type id: int
    :param name: user_name
    :type name: string
    """
    # connect to database
    conn = db_connect_open()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * from JLHNSONLhK.{users_table_name} WHERE user_id={id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        cursor.execute(f"UPDATE JLHNSONLhK.{users_table_name} SET user_name='{name}' WHERE user_id={id}")
        conn.commit()

    except pymysql.err.Error as e:
        raise e

def db_delete_user(id):
    """
    Delete user with specified id from the database
    :param id: user_id
    :type id: int
    """
    # connect to database
    conn = db_connect_open()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * from JLHNSONLhK.{users_table_name} WHERE user_id={id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        cursor.execute(f"DELETE from JLHNSONLhK.{users_table_name} WHERE user_id={id}")
        conn.commit()

    except pymysql.err.Error as e:
        raise e

def db_get_max_user_id():
    """
    Returns maximum user_id found in users table
    :return: maximum user_id
    :rtype: int
    """
    # connect to database
    conn = db_connect_open()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT max(user_id) from {users_table_name}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Fail in getting max user id")
        if row[0] == None:
            return 0
        return row[0]
    except pymysql.err.Error as e:
        raise e

    finally:
        db_connect_close(conn, cursor)

def db_get_all_tests_config():
    """
    Connect to config table and brings all rows. These are all tests that should be performed by application.
    Each test will have different browser and user_name that should be inserted
    :return: list of all tests that should be performed
    :rtype: list of tuples
    """
    # connect to database
    conn = db_connect_open()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * from JLHNSONLhK.{config_table_name}")
        all_tests = cursor.fetchall()
        return all_tests
    except pymysql.err.Error as e:
        raise e

    finally:
        db_connect_close(conn, cursor)
