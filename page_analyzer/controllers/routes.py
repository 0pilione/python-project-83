from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint, get_flashed_messages
from dotenv import load_dotenv
import os
from page_analyzer.models.repo import UrlRepository
import psycopg2
import validators
from validators import length
import urllib.parse
from datetime import datetime
from urllib.parse import urlparse, urlunparse



# Инициализация приложения Flask

main_page = Blueprint('/', __name__, template_folder='templates')
load_dotenv()
#app = Flask(__name__, template_folder='templates')
url = os.environ.get('DATABASE_URL')
parsed_url = urllib.parse.urlparse(url)
params = {
    "database": parsed_url.path.lstrip('/'),  
    "user": parsed_url.username,               
    "password": parsed_url.password,           
    "host": parsed_url.hostname,               
    "port": parsed_url.port                    
}

conn = psycopg2.connect(**params)



@main_page.route("/", methods=["POST", "GET"])
def m():
    repo = UrlRepository(conn)
    if request.method == 'POST':
        data = request.form.to_dict()
        current_time = datetime.now()
        lower_case_url = data['url'].lower()
        parsed_url = urlparse(lower_case_url)
        
        components = (
        parsed_url.scheme or 'https',           
        parsed_url.netloc.rstrip(':80').rstrip(':443'),  
        parsed_url.path.rstrip('/'),           
        '',                                   
        parsed_url.query,                     
        '')
        normalized_url = urlunparse(components)
        try:
            length(normalized_url, min=3, max=255)
            url = {"name": normalized_url, 'created_at': current_time}
            existing_urls = [u['name'] for u in repo.get_content()]
            existing_id = repo.get_specific_id(url['name'])
            if url['name'] not in existing_urls:
                repo.save(url)
                existing = repo.get_specific_id(url['name'])
                flash("Страница успешно добавлена", "success")
                conn.close()
                return redirect(url_for('/.url_id', id=existing[0]['id']))
            else:
                flash("Страница уже существует", "error")
                conn.close()
                return redirect(url_for('/.url_id', id=existing_id[0]['id']))
        except Exception as e:     
            flash("URL превышает 255 символов", "error")
            conn.close()
            return render_template('index.html'), 422
    else:
        conn.close()
        return render_template('index.html'), 200
    

@main_page.route('/urls', methods=['GET'])
def url_list():
    repo = UrlRepository(conn)
    k = repo.get_content()
    v = m()
    conn.close()
    return render_template('//urls.html', k=k, m=v[1])

@main_page.route('/urls/<id>', methods=['GET'])
def url_id(id):
    repo = UrlRepository(conn)
    k = repo.get_id(id)
    conn.close()
    return render_template('//url.html', b=k)
    
