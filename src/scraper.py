from typing import Any
from .course import CourseInfo
from src.network import make_requests
from .utils import generate_course_url
from .errors import ParsingTitleError
from bs4 import BeautifulSoup


# TODO: Fix the scrape function to extract "Eixo Tecnologico" and course schools data
def _parse_page(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, "html.parser")


def scrape_all_courses(html: BeautifulSoup) -> list[dict[str, Any]]:
    courses = []

    course_page_elements = html.select("div.listagem-posts-conteudos")
    print("Inicializando Extração das Informações...")
    for course in course_page_elements:
        title = course.select_one("h3.listagem-posts-titulo")
        if not title:
            raise ParsingTitleError("Could Not Parse the Title")

        title = title.get_text(strip=True)
        modalities = [
            tag.get_text(strip=True) for tag in course.select("span.term-lista-tipo")
        ]
        detailed_info = navigate_and_extract_detailed_info(title)
        print(detailed_info)
        course_data = CourseInfo(title=title, modalities=modalities, **detailed_info)
        courses.append(course_data)

    return courses


def navigate_and_extract_detailed_info(title: str):
    url = generate_course_url(title)
    content = make_requests(url)
    page = _parse_page(content)
    info = scrape_specific_course_info(page)
    return info


def scrape_specific_course_info(page: BeautifulSoup) -> dict[str, Any]:
    details = {}

    description = page.select_one("div.descricao-curso > p")
    details["description"] = description.get_text(strip=True) if description else ""

    details["workload"] = "Não Informado"
    details["semesters"] = "Não Informado"
    details["course_field"] = "Não Informado"

    course_info = page.select("div.observacoes-curso > div > p")

    if len(course_info) > 0:
        details["workload"] = (
            course_info[0].get_text(strip=True).replace("Carga horária", "").strip()
        )

    if len(course_info) > 1:
        details["semesters"] = (
            course_info[1].get_text(strip=True).replace("Semestres", "").strip()
        )

    if len(course_info) > 3:
        a_tag = course_info[3].find("a")

        if a_tag:
            details["course_field"] = (
                a_tag.get_text(strip=True).replace("Eixo tecnológico", "").strip()
            )

    course_text = page.select("div.right-column-cursos > p")

    if len(course_text) > 0:
        details["course_area"] = (
            course_text[0].get_text(strip=True).replace("Área de Atuação", "").strip()
        )

    if len(course_text) > 1:
        details["where_to_work"] = (
            course_text[1].get_text(strip=True).replace("Onde Trabalhar:", "").strip()
        )

    details["where_to_study"] = [
        tag.get_text(strip=True)
        for tag in page.select("p.panel-presencial > a > span.title-unidades-cursos")
    ]

    return details
