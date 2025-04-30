from flask import Flask, flash, redirect, url_for, get_flashed_messages
from page_analyzer.models.check_repo import UrlCheckRepository
from page_analyzer.models.repo import UrlRepository
from datetime import datetime
import requests
from page_analyzer.controllers.parsed_tags import ParsedTags
from page_analyzer.controllers.parsed_url import conn, check_page


@check_page.route('/urls/<int:id>/checks', methods=['POST'])
def save_check(id):
    current_time = datetime.now()
    repo = UrlCheckRepository(conn)
    response = check_response(id)
    parsed_tags = ParsedTags(id, conn)
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
    repo = UrlRepository(conn)
    get_check = repo.get_id(id)
    for check in get_check:
        check_name = check['name']
    try:
        response = requests.get(check_name, timeout=10)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        return 'failed request'
    except Exception as e:
        return 'failed'