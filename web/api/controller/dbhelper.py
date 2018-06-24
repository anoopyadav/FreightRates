import psycopg2
import os


def connect_db():
    if 'local' in os.environ:
        host = '0.0.0.0'
    else:
        host = 'db'
    try:
        connection = psycopg2.connect("dbname='postgres' user='postgres' host='{0}' password='password'".format(host))
    except TypeError:
        raise Exception("Can't connect to DB")

    return connection


def execute_query():
    return
