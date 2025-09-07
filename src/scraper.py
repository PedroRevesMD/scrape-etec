from typing import Any

from .course import CourseInfo
from src.network import make_requests
from .utils import _get_clean_value, generate_course_url
from .errors import ParsingTitleError
from bs4 import BeautifulSoup


def _parse_page(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, "html.parser")


def scrape_all_courses(html: BeautifulSoup) -> list[dict[str, Any]]:
    courses = []

    course_page_elements = html.select("div.listagem-posts-conteudos")

    for course in course_page_elements:
        title = course.select_one("h3.listagem-posts-titulo")
        if not title:
            raise ParsingTitleError("Could Not Parse the Title")

        title = title.get_text(strip=True)
        modalities = [
            tag.get_text(strip=True) for tag in course.select("span.term-lista-tipo")
        ]
        detailed_info = navigate_and_extract_detailed_info(title)
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

    details["workload"] = ""
    details["semesters"] = ""
    details["course_field"] = ""

    course_info = page.select("div.observacoes-curso > p")

    for info in course_info:
        text = info.get_text(strip=True)
        if "Carga horária:" in text:
            details["workload"] = _get_clean_value(text, "Carga horária:")
        elif "Semestres:" in text:
            details["semesters"] = _get_clean_value(text, "Semestres:")
        elif "Eixo Tecnológico:" in text:
            details["course_field"] = _get_clean_value(text, "Eixo Tecnológico:")

    work_container = page.select_one("div.right-column-cursos")

    if work_container:
        work_paragraphs = work_container.find_all("p")
        if len(work_paragraphs) > 0:
            details["course_area"] = work_paragraphs[0].get_text(
                strip=True, separator="\n"
            )
        if len(work_paragraphs) > 1:
            details["where_to_work"] = work_paragraphs[1].get_text(
                strip=True, separator="\n"
            )

    details["where_to_study"] = [
        tag.get_text(strip=True)
        for tag in page.select("div.panel-presencial > span.title-unidades-cursos")
    ]

    return details
