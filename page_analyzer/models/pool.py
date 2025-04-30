import os
import urllib.parse

from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()
url = os.environ.get('DATABASE_URL')
host = os.environ.get('HOST')
parsed_url = urllib.parse.urlparse(url)
params = {
    "database": parsed_url.path.lstrip('/'),  
    "user": parsed_url.username,               
    "password": parsed_url.password,           
    "host": parsed_url.hostname,               
    "port": parsed_url.port                    
}
dsn_string = "dbname={database} user={user} password={password} host={host}".format(**params)
db_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, dsn=dsn_string)