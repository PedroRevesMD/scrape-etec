import requests


def make_requests(url: str, timeout: int = 3):
    page = requests.get(url, timeout=timeout)
    page.raise_for_status()
    return page.text
