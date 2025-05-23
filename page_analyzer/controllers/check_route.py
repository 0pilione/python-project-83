from datetime import datetime

import requests
from flask import (Flask, flash, get_flashed_messages, redirect,  # noqa: F401
                   url_for)

from page_analyzer.controllers.parsed_tags import ParsedTags
from page_analyzer.controllers.parsed_url import check_page, conn
from page_analyzer.models.check_repo import UrlCheckRepository
from page_analyzer.models.repo import UrlRepository


@check_page.route('/urls/<int:id>/checks', methods=['POST'])
def save_check(id):
    '''Сохраняет проверку'''
    current_time = datetime.now()
    repo = UrlCheckRepository()
    response = check_response(id)
    parsed_tags = ParsedTags(id)
    if isinstance(response, str):
        flash("Произошла ошибка при проверке", "danger")
    else:
        check = {
            "url_id": id,
            'status_code': response,
            'h1': parsed_tags.h1(),
            'title': parsed_tags.title(),
            'description': parsed_tags.description(),
            'created_at': current_time
        }
        repo.save(check)
        flash("Страница успешно проверена", "success")
    conn.close()
    return redirect(url_for('/.url_id', id=id))


def check_response(id):
    '''Выполняет проверку доступности URL-адреса'''
    repo = UrlRepository()
    get_check = repo.get_id(id)
    for check in get_check:
        check_name = check['name']
    try:
        response = requests.get(check_name, timeout=10)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException:
        return 'failed request'
    except Exception:
        return 'failed'
