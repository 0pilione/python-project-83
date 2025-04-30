from page_analyzer.models.repo import UrlRepository
import requests
from bs4 import BeautifulSoup



class ParsedTags:
    
    def __init__(self, id, conn):
        self.conn = conn
        self.repo = UrlRepository(self.conn)
        self.id = id
        
    def base(self):
        content = self.repo.get_id(self.id)
        for name in content:
            url_name = name['name']
            response = requests.get(url_name)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        
    def h1(self):
        h1_tag = self.base().find('h1')
        if h1_tag:
            return h1_tag.text.strip()
        else:
            return None
    
    def title(self):
        title_tag = self.base().find('title')
        if title_tag:
            return title_tag.text.strip()
        else:
            return None

    def description(self):
        element = self.base().find('meta', attrs={'name': 'description', 'content': True})
        if element:
            if 'content' in element.attrs:
                return element.get('content')