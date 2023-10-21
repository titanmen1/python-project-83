from urllib.parse import urlparse


def parse_url(url):
    return f"{urlparse(url).scheme}://{urlparse(url).netloc}"
