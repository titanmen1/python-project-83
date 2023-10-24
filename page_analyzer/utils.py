from urllib.parse import urlparse

import requests as requests
from bs4 import BeautifulSoup


def parse_url(url):
    return f"{urlparse(url).scheme}://{urlparse(url).netloc}"


def get_site_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    status_code = page.status_code

    if status_code == 200:
        h1 = soup.find('h1').get_text() if soup.find('h1') else ''
        title = soup.find('title').get_text() if soup.find('title') else ''
        description = (
            soup.find(attrs=({'name': 'description'})).get('content')
            if soup.find(attrs=({'name': 'description'}))
            else ''
        )
        result = {'h1': h1, 'title': title, 'description': description, 'status_code': status_code}
        return result
    else:
        return False
