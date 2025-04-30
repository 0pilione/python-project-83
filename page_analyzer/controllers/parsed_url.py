from flask import Blueprint
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import psycopg2

check_page = Blueprint('checks', __name__, template_folder='templates')
main_page = Blueprint('/', __name__, template_folder='templates')
load_dotenv()
url = os.environ.get('DATABASE_URL')
parsed_url = urlparse(url)
params = {
    "database": parsed_url.path.lstrip('/'),  
    "user": parsed_url.username,               
    "password": parsed_url.password,           
    "host": parsed_url.hostname,               
    "port": parsed_url.port                    
}

conn = psycopg2.connect(**params)