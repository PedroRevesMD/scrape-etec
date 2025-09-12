import requests
import logging
from requests.exceptions import ConnectionError, Timeout


def make_requests(url: str, timeout: int = 10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    try:
        page = requests.get(url, timeout=timeout, headers=headers)
        page.raise_for_status()
        return page.text
    except ConnectionError:
        logging.warning(f"Erro ao fazer requisição para {url}")
        raise
    except Timeout:
        logging.warning(f"Timeout ao acessar {url}")
        raise
