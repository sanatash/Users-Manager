from datetime import datetime
import pymysql


def db_connect_open():
    """
    Opens connection to the MySql database
    :return: connection object
    :rtype: Connector class
    """
    try:
        # Establishing a connection to DB
        conn = pymysql.connect(host='remotemysql.com', port=3306, user='JLHNSONLhK', passwd='HE6DJPd5an',
                               db='JLHNSONLhK')
        conn.autocommit(True)
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
    cursor = conn.cursor()

    try:
        # Current date time in local system
        creation_date = datetime.now().replace(microsecond=0)
        # Inserting data into table
        cursor.execute(
            f"INSERT into JLHNSONLhK.users (user_id, user_name, creation_date) VALUES ({id}, '{name}', '{creation_date}')")
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
        # Inserting data into table
        cursor.execute(f"SELECT user_name from JLHNSONLhK.users WHERE user_id = {id}")
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
        cursor.execute(f"SELECT * from JLHNSONLhK.users WHERE user_id={id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        cursor.execute(f"UPDATE JLHNSONLhK.users SET user_name='{name}' WHERE user_id={id}")

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
        cursor.execute(f"SELECT * from JLHNSONLhK.users WHERE user_id={id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        cursor.execute(f"DELETE from JLHNSONLhK.users WHERE user_id={id}")

    except pymysql.err.Error as e:
        raise e

