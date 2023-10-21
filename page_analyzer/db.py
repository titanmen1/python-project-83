import datetime

import psycopg2
from psycopg2.extras import NamedTupleCursor


def get_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


def check_url_exists(connection, url):
    query = f"SELECT EXISTS (SELECT name FROM urls WHERE name='{url}');"

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(query)
        return cursor.fetchone().exists



def insert_url(connection, url):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            f"INSERT INTO urls (name, created_at) VALUES ('{url}', '{datetime.datetime.now()}') RETURNING id;",
        )
        url_id = cursor.fetchone().id
    connection.commit()
    return url_id


def get_url_by_id(connection, url_id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(f'SELECT id, name FROM urls WHERE id={url_id}')
        url = cursor.fetchone()
    return url

def get_url_by_name(connection, url_name):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(f'SELECT id, name FROM urls WHERE name={url_name}')
        url = cursor.fetchone()
    return url

def get_checks_info_of_url(connection, url_id):

    query = f'''SELECT id, status_code, h1, title, description, DATE(created_at)
            FROM url_checks
            WHERE url_id='{url_id}'
            ORDER BY id DESC'''

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(query)
        return cursor.fetchall()
