# app/my_api/database.py

import psycopg2
import os

from .schema import queries, admin


def database():
    db_url = os.getenv('DATABASE_URL')
    # connect with psycopg2
    conn = psycopg2.connect(db_url)
    return conn


def database_init():
    # create tables
    connection = database()
    connection.autocommit = True
    cur = connection.cursor()
    try:
        for query in queries:
            if query:
                cur.execute(query)
        cur.execute(admin)
    except (Exception, psycopg2.DatabaseError) as error:
        cur.execute("rollback;")
        print(error)
        return {'Message': 'current transaction is aborted'}, 500
