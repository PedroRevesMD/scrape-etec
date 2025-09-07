import time

from src.network import make_requests
from src.scraper import _parse_page, scrape_all_courses

url = "https://www.cps.sp.gov.br/etec/cursos-oferecidos-pelas-etecs/"


def main():
    print("Iniciando Scraping de Cursos...")
    time.sleep(2)
    print("Realizando request para a Página...")
    content = make_requests(url)
    time.sleep(1)
    print("Fazendo Parsing da Página...")
    page = _parse_page(content)
    time.sleep(1)
    print("Selecionando as Informações...")
    time.sleep(1)
    info = scrape_all_courses(page)
    total_courses = len(info)

    if total_courses < 1:
        print("Erro: Não foi possível extrair as informações dos cursos...")

    print(info)


if __name__ == "__main__":
    main()
