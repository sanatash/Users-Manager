"""
Database module which connect to MySQL database and performs various SQL operations
"""

from datetime import datetime
import pymysql
import mysql.connector

def db_connect_open():
    """
    Opens connection to the MySql database
    :return: connection object
    :rtype: Connector class
    """
    try:
        # Establishing a connection to DB
        conn = mysql.connector.connect(host= 'remotemysql.com', port=3307, user='JLHNSONLhK',
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
        creation_date = datetime.now().replace(microsecond=0)
        # Parameterized query
        sql_insert_query = """INSERT into JLHNSONLhK.users (user_id, user_name, creation_date)
                            VALUES (%s, %s, %s)"""
        # tuple to insert at placeholder
        tuple = (id, name, creation_date)
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
        cursor.execute(f"SELECT * from JLHNSONLhK.users WHERE user_id={id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        cursor.execute(f"DELETE from JLHNSONLhK.users WHERE user_id={id}")
        conn.commit()

    except pymysql.err.Error as e:
        raise e
