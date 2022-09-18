"""
Database module which connect to MySQL database and performs various SQL operations
"""
import pymysql
import mysql.connector
from configobj import ConfigObj

db_host = 'mysql'
db_port = 3306
db_user = 'root'
db_passwd = ''
mysql_database = ''

# Tables
users_table_name = "users"
config_table_name = "config"

def db_save_credentials(user, password):
    """
    Stores database user name and password credentials in module global variables
    :param user: database user
    :type user: string
    :param password: database password
    :type password:  string
    """
    global db_user
    db_user = user
    global db_passwd
    db_passwd = password

def db_get_mysql_details():
    conf = ConfigObj('mysql.env')
    global mysql_database
    mysql_database = conf['MYSQL_DATABASE']
    global db_passwd
    db_passwd = conf['MYSQL_ROOT_PASSWORD']

def db_connect_open():
    """
    Opens connection to the MySql database
    :return: connection object
    :rtype: Connector class
    """
    db_get_mysql_details()

    try:
        # Establishing a connection to DB
        conn = mysql.connector.connect(host= db_host, port=db_port, user=db_user, passwd=db_passwd , database=mysql_database)
        return conn

    except Exception as e:
        print(f"exception: {e}")
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

        print(mysql_database)
        sql_insert_query = f"""INSERT into {mysql_database}.{users_table_name} (user_id, user_name)
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
        print(f"{mysql_database}.{users_table_name}")
        cursor.execute(f"SELECT user_name from {mysql_database}.{users_table_name} WHERE user_id = {id}")
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
    Changes user name accordingly to user id in database3
    :param id: user_id
    :type id: int
    :param name: user_namedb_insert_user
    :type name: string
    """
    # connect to database
    conn = db_connect_open()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * from {mysql_database}.{users_table_name} WHERE user_id={id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        cursor.execute(f"UPDATE {mysql_database}.{users_table_name} SET user_name='{name}' WHERE user_id={id}")
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
        cursor.execute(f"SELECT * from {mysql_database}.{users_table_name} WHERE user_id={id}")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No such Id")
        cursor.execute(f"DELETE from {mysql_database}.{users_table_name} WHERE user_id={id}")
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
        cursor.execute(f"SELECT * from {mysql_database}.{config_table_name}")
        all_tests = cursor.fetchall()
        return all_tests
    except Exception as error:#pymysql.err.Error as e:
        print(f"db_docker_connect {error}")
        raise error

    finally:
        db_connect_close(conn, cursor)
