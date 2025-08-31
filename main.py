import requests
from bs4 import BeautifulSoup


def make_requests(url: str, timeout: int = 3):
    page = requests.get(url, timeout=timeout)
    page.raise_for_status()
    return page


def main():
    make_requests("https://www.cps.sp.gov.br/etec/cursos-oferecidos-pelas-etecs/")


if __name__ == "__main__":
    main()
