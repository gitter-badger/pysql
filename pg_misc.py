#!/usr/bin/env python
"""
    pg_misc.py: A bunch of sql utilities from information_schema.
"""

import argparse
from argparse import RawTextHelpFormatter
import psycopg2.extras
import psycopg2
from prettytable import PrettyTable
from subprocess import call


__author__ = "Flores, Facundo Gabriel"
__email__ = "flores.facundogabriel@gmail.com"
__version__ = "1.0"
__status__ = "Development"


DB_INFO = {
    "NAME": "suit",
    "USER": "postgres",
    "PASSWORD": "123456",
    "HOST": "192.168.0.8",
    "SCHEMA": "public",
}


def show_pretty(fetched_query):
    columns_names = fetched_query[0].keys()
    t = PrettyTable(columns_names)
    """all coumns align to left"""
    for k in columns_names:
        t.align[k] = 'l'
    for r in fetched_query:
        tmp_row = []
        for k in columns_names:
            tmp_row.append(r[k])
        t.add_row(tmp_row)
    """printing data in editor"""
    data = t.get_string()
    with open('out.txt', 'wb') as f:
        f.write(data)
    call(["atom", "out.txt"]) #change to nano if you want


def __get_tables_with_unique_constraint(cursor):
    query = """ SELECT table_name, constraint_name
                    FROM information_schema.table_constraints
                    WHERE constraint_type = 'UNIQUE' AND
                    table_schema = 'public';
            """
    cursor.execute(query)
    return cursor.fetchall()


def show_tables_with_unique_constraint(conn):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    rows = __get_tables_with_unique_constraint(cur)
    show_pretty(rows)


def __get_custom_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


def custom_query(conn, query):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    rows = __get_custom_query(cur, query)
    show_pretty(rows)


def bye():
    print "Bye!"


def pg_connect():
    connection = "dbname=" + DB_INFO["NAME"] + " "
    connection += "user=" + DB_INFO["USER"] + " "
    connection += "host=" + DB_INFO["HOST"] + " "
    connection += "password=" + DB_INFO["PASSWORD"]
    return psycopg2.connect(connection)


def test_connection_todb():
    try:
        conn = pg_connect()
        print "I am connected to " + DB_INFO["NAME"] + " " + DB_INFO["HOST"]
    except:
        print "I am unable to connect to the database"


def main():
    OPTIONS = {
        "1": custom_query,
        "2": show_tables_with_unique_constraint,
        "0": bye
    }

    app_description = "Execute some queries from information_schema \n"
    app_description += """
                        1- Custom Query
                        2- Show tables with unique constraints
                        3-
                        0- EXIT
                    """
    parser = argparse.ArgumentParser(description=app_description,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('opt',  help="Choice an option")
    parser.add_argument('query', nargs='?', help="Custom Query")
    args = parser.parse_args()
    try:
        conn = pg_connect()
        print "I am connected to " + DB_INFO["NAME"] + " " + DB_INFO["HOST"]
    except:
        print "I am unable to connect to the database"

    if args.opt == "1":
        custom_query(conn, args.query)
    else:
        OPTIONS[args.opt](conn)


if __name__ == '__main__':
    main()
