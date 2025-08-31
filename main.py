import requests
from bs4 import BeautifulSoup


def make_requests(url: str, timeout: int = 3):
    page = requests.get(url, timeout=timeout)
    page.raise_for_status()
    return page.text


def parse_page(page: str) -> BeautifulSoup:
    content = BeautifulSoup(page, "html.parser")
    print(content.prettify())
    return content


def main():
    page = make_requests(
        "https://www.cps.sp.gov.br/etec/cursos-oferecidos-pelas-etecs/"
    )
    content = parse_page(page)
    print(content)


if __name__ == "__main__":
    main()
