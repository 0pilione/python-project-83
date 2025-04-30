from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint, get_flashed_messages
from page_analyzer.models.repo import UrlRepository
from validators import length
import urllib.parse
from datetime import datetime
from urllib.parse import urlparse, urlunparse
from page_analyzer.models.check_repo import UrlCheckRepository
import requests
from page_analyzer.controllers.parsed_url import conn, main_page


@main_page.route("/", methods=["POST", "GET"])
def save_url():
    if request.method == 'POST':
        repo = UrlRepository(conn)
        data = request.form.to_dict()
        url = normalized_url(data)
        current_time = datetime.now()
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
        except Exception as e:     
            flash("URL превышает 255 символов", "danger")
            conn.close()
            return render_template('index.html')
    else:
        conn.close()
        return render_template('index.html')
    

def normalized_url(data):
    lower_case_url = data['url'].lower()
    parsed_url = urlparse(lower_case_url)
    components = (
        parsed_url.scheme or 'https',           
        parsed_url.netloc.rstrip(':80').rstrip(':443'),  
        parsed_url.path.rstrip('/'),           
        '',                                   
        parsed_url.query,                     
        ''
    )
    normalized_url = urlunparse(components)
    return normalized_url

@main_page.route('/urls', methods=['GET'])
def url_list():
    repo = UrlRepository(conn)
    repo_2 = UrlCheckRepository(conn)
    content = repo.get_content()
    url_list = [repo_2.get_check_id(check['id']) for check in content]
    conn.close()  
    return render_template('urls.html', content=content, urls=url_list)

@main_page.route('/urls/<id>', methods=['GET'])
def url_id(id):
    repo = UrlRepository(conn)
    repo_2 = UrlCheckRepository(conn)
    check_id = repo_2.get_check_id(id)
    url = repo.get_id(id)
    conn.close()
    return render_template('//url.html', url_id=url, check_id=check_id)

