import requests
import logging
from requests.exceptions import ConnectionError, Timeout

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,*/*;q=0.9",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def make_requests(url: str, timeout: int = 15) -> str:
    try:
        page = requests.get(url, timeout=timeout, headers=HEADERS)
        page.raise_for_status()
        return page.text
    except ConnectionError:
        logging.warning(f"Erro ao fazer requisição para {url}")
        raise
    except Timeout:
        logging.warning(f"Timeout ao acessar {url}")
        raise
