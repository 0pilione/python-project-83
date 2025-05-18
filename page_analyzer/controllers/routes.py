import urllib  # noqa: F401
from datetime import datetime
from urllib.parse import urlparse, urlunparse

import requests  # noqa: F401
from flask import (Flask, flash, get_flashed_messages, redirect,  # noqa: F401
                   render_template, request, url_for, session)
from validators import length
from validators import url as validate_url
from validators.utils import ValidationError

from page_analyzer.controllers.parsed_url import conn, main_page
from page_analyzer.models.check_repo import UrlCheckRepository
from page_analyzer.models.repo import UrlRepository


@main_page.route("/", methods=["POST", "GET"])
def save_url():
    if request.method == 'POST':
        repo = UrlRepository()
        data = request.form.to_dict()
        url = normalized_url(data)
        current_time = datetime.now()
        if not is_valid_url(data['url']):
            flash("Некорректный URL", "danger")
            session['from_uncorrect_url'] = True
            return redirect(url_for('/.url_list'))
        try:
            length(url, min=3, max=255)
            url = {"name": url,  'created_at': current_time}
            existing_urls = [u['name'] for u in repo.get_content()]
            existing_id = repo.get_specific_id(url['name'])
            if url['name'] not in existing_urls:
                repo.save(url)
                existing = repo.get_specific_id(url['name'])
                flash("Страница успешно добавлена", "success")
                conn.close()
                return redirect(url_for('/.url_id', id=existing[0]['id']))
            else:
                flash("Страница уже существует", "danger")
                conn.close()
                return redirect(url_for('/.url_id', id=existing_id[0]['id']))
        except Exception:
            flash("URL превышает 255 символов", "danger")
            conn.close()
            return render_template('index.html')
    else:
        conn.close()
        return render_template('index.html')


def is_valid_url(url):
    """Проверка URL с помощью библиотеки validators"""
    try:
        return validate_url(url)
    except ValidationError:
        return False


def normalized_url(data):
    lower_case_url = data['url'].lower()
    parsed_url = urlparse(lower_case_url)
    components = (
        parsed_url.scheme or 'https',
        parsed_url.netloc.rstrip(':80').rstrip(':443'),
        '',
        '',
        '',
        ''
    )
    normalized_url = urlunparse(components)
    return normalized_url


@main_page.route('/urls', methods=['POST'])
def uncorrect_url():
    data = request.form.to_dict()
    if not is_valid_url(data['url']):
        conn.close()
        return render_template('index.html')


@main_page.route('/urls', methods=['GET'])
def url_list():
    if session.pop('from_uncorrect_url', False):
        return render_template('index.html')
    repo = UrlRepository()
    repo_2 = UrlCheckRepository()
    content = repo.get_content()
    url_list = [repo_2.get_check_id(check['id']) for check in content]
    conn.close()
    return render_template('urls.html', content=content, urls=url_list)


@main_page.route('/urls/<id>', methods=['GET'])
def url_id(id):
    repo = UrlRepository()
    repo_2 = UrlCheckRepository()
    check_id = repo_2.get_check_id(id)
    url = repo.get_id(id)
    conn.close()
    return render_template('//url.html', url_id=url, check_id=check_id)
