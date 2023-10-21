import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from validators import url

from page_analyzer import db
from page_analyzer.utils import parse_url

load_dotenv()
app = Flask(__name__)

app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = psycopg2.connect(app.config['DATABASE_URL'])


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def post_url_for_checking():
    url_for_checking = request.form['url']
    if not url_for_checking:
        flash('URL обязателен для ввода')
        return render_template('index.html')

    parsed_url = parse_url(url_for_checking)
    validated_url = url(parsed_url)

    if not validated_url:
        flash('Некорректный URL')
        return render_template('index.html'), 422

    connection = db.get_db(app)
    is_url_exists = db.check_url_exists(connection, parsed_url)

    if not is_url_exists:
        url_id = db.insert_url(connection, parsed_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', url_id=url_id))
    else:
        url_id = 5
        return redirect(url_for('get_url', url_id=url_id))


@app.route('/urls/<url_id>', methods=['GET'])
def get_url(url_id):
    connection = db.get_db(app)
    url_info = db.get_url_by_id(connection, url_id)
    checks_list = db.get_checks_info_of_url(connection, url_id)

    return render_template('url_info.html', url_info=url_info, checks_list=checks_list)