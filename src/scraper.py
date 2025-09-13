from typing import Any
from .course import CourseInfo
from src.network import make_requests
from .utils import generate_course_url, remove_schools_duplicates
from .errors import ParsingTitleError
from bs4 import BeautifulSoup


def parse_page(html_content: str) -> BeautifulSoup:
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
    print(url)
    content = make_requests(url)
    page = parse_page(content)
    info = scrape_specific_course_info(page)
    return info


def scrape_specific_course_info(page: BeautifulSoup) -> dict[str, Any]:
    details = {}

    description_list = page.select("div.descricao-curso > p")
    text: list[str] = []
    for description in description_list:
        content = description.get_text(strip=True) if description else ""
        text.append(content)
        details["description"] = "\n\n".join(text)

    details["workload"] = "Não Informado"
    details["semesters"] = "Não Informado"
    details["course_field"] = "Não Informado"
    details["where_to_work"] = "Não Informado"
    details["course_area"] = "Não Informado"
    details["where_to_study"] = "Não Informado"
    details["requirements"] = "Não Informado"

    course_info = page.select("div.observacoes-curso > div > p")
    print(f"DEBUG: Encontrados {len(course_info)} elementos em course_info")

    if len(course_info) > 0:
        details["workload"] = (
            course_info[0].get_text(strip=True).replace("Carga horária", "").strip()
        )

    if len(course_info) > 1:
        details["semesters"] = (
            course_info[1].get_text(strip=True).replace("Semestres", "")
        )

    if len(course_info) > 2:
        a_tag = course_info[2].find("a")

        if a_tag:
            details["course_field"] = a_tag.get_text(strip=True).replace(
                "Eixo tecnológico", ""
            )

    course_paragraphs = page.select("div.detalhes-cursos")
    for paragraph in course_paragraphs:
        paragraph_title = paragraph.select_one("div.detalhes-cursos > h3")
        if paragraph_title:
            paragraph_title = paragraph_title.get_text(strip=True)
        else:
            continue

        paragraph_text = paragraph.select(
            "div.detalhes-cursos > div.right-column-cursos > p"
        )

        if paragraph_text:
            p_text = " ".join([p.get_text(strip=True) for p in paragraph_text])
        else:
            continue

        if "Área " in paragraph_title and "Atuação":
            details["course_area"] = p_text
        if "Onde" in paragraph_title and "Trabalhar":
            details["where_to_work"] = p_text
        if "requisitos" in paragraph_title:
            details["requirements"] = p_text

    schools = [
        tag.get_text(strip=True) for tag in page.select("span.title-unidades-cursos")
    ]
    details["where_to_study"] = remove_schools_duplicates(schools)
    return details


def check_if_string_contains_text(string: str) -> bool:
    return "Área " in string or "Onde" in string or "Requisitos " in string
