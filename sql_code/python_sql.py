"""
Library to interact with a SQLite Database
"""

import sqlite3
import os


# Following are for running general SQLite queries
def query_existing(src_cursor):
    """
    Function to get table information from existing sqlite DB
    src_cursor - connection to DB
    Returns
    tables - list of tables in database
    """
    try:
        src_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = src_cursor.fetchall()
    except sqlite3.Error as error:
        print(
            "Error while requesting \n SELECT name FROM sqlite_master WHERE type='table'; \n",
            error,
        )

    return tables


def query_table_schema(src_cursor, tablename):
    """
    Function to get table schemas
    src_cursor - connection to DB
    tablename - name of table to query schema from
    Returns
    Just prints list to screen
    """
    try:
        src_cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{tablename}';")
        print(f"Table {tablename} created with following schema:")
        tab_schema = src_cursor.fetchall()[0]
        print(tab_schema)
        return tab_schema
    except sqlite3.Error as error:
        print(
            f"Error while requesting \n SELECT sql FROM sqlite_schema WHERE name={tablename}; \n",
            error,
        )

def connect_db(db_name, db_create, setstring="", rowfactory=None):
    """Connect to target database

    Args:
        db_name (str): Name or full file path to database
        db_create (int): Whether to create database or not, 1 creates
        setstring (str, optional): Any commands that should be run at beginning of creation of db (e.g a pragma). Defaults to "".

    Returns:
        error, connect, curs: Whether conneciton has been made 0 good, -1 not found
    """

    # Set up the row factory to return dictionary not tuple if required
    if rowfactory == "Row":
        rowfactory = sqlite3.Row
    try:
        # check the database exists or we want new
        if os.path.isfile(db_name) or (db_create == 1):
            connect = sqlite3.connect(db_name)
            connect.row_factory = rowfactory
            curs = connect.cursor()
            error = 0
            # run set string command if given
            if setstring:
                curs.execute(setstring)
            return error, connect, curs
        else:
            error = -1
            return error, 0, 0

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return error, connect, curs


def run_sql(src_cursor, select_text):
    """Function to run any SQLite command
    No attempt is made to sanitise the input, will run as is

    Args:
        src_cursor (sqlite cursor): Cursor to the sqlite database
        select_text (str): the preformtated SQL command

    Returns:
        int: Whether command was successful or not
    """
    try:
        src_cursor.execute(select_text)
        return 1
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return -1


def select_existing(src_cursor, select_text):
    """
    Function to get information from existing sqlite DB
    src_cursor - connection to DB
    select_text - text to send to DB, must be a SELECT
    Returns
    tables - list of tables in database
    """
    try:
        # src_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        src_cursor.execute(select_text)
        tables = src_cursor.fetchall()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return tables


def select_existing_dict(src_cursor, select_text):
    """
    Function to get information from existing sqlite DB
    src_cursor - connection to DB
    select_text - text to send to DB, must be a SELECT
    Returns
    tables - dict of results in database
    """
    try:
        # src_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        src_cursor.execute(select_text)

        tables = src_cursor.fetchall()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return tables