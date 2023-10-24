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
        cursor.execute(f"SELECT id, name FROM urls WHERE name='{url_name}'")
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


def insert_checks_result(connection, url_id, checks_result):
    status_code = checks_result['status_code']
    h1 = checks_result['h1']
    title = checks_result['title']
    description = checks_result['description']

    query = (
        f'''INSERT INTO url_checks (url_id, status_code, h1, title, description)
            VALUES ({url_id}, {status_code}, '{h1}', '{title}', '{description}');'''
    )

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(query)
    connection.commit()


def get_urls_with_checks(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM urls ORDER BY id DESC;',
        )
        urls = curs.fetchall()  # noqa: WPS442
        curs.execute(
            'SELECT DISTINCT ON (url_id) * FROM url_checks ORDER BY url_id DESC, created_at ASC;',
        )
        checks = curs.fetchall()

    result = []
    checks_by_url_id = {check.url_id: check for check in checks}
    for url in urls:
        url_data = {}
        check = checks_by_url_id.get(url.id)
        url_data['id'] = url.id
        url_data['name'] = url.name
        url_data['last_check_date'] = check.created_at if check else ''
        url_data['status_code'] = check.status_code if check else ''
        result.append(url_data)

    return result
