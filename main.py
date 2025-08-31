import requests
import regex as re
import unicodedata
from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup


@dataclass
class CourseInfo:
    title: str
    modalities: List[str]
    description: str
    workload: int
    semesters: int
    course_area: str
    course_field: str
    where_to_work: str
    where_to_study: List[str]


def make_requests(url: str, timeout: int = 3):
    page = requests.get(url, timeout=timeout)
    page.raise_for_status()
    return page.text


def parse_page(html_content: str) -> BeautifulSoup:
    if not html_content or not html_content.strip():
        raise ValueError("Error: HTML page cannot be empty")
    try:
        content = BeautifulSoup(html_content, "html.parser")
    except Exception as e:
        raise ValueError(f"Cannot parse website. Try Again! {e}") from e

    return content


def select_course_info(html: BeautifulSoup) -> List[CourseInfo]:
    courses: List[CourseInfo] = []

    course_page_elements = html.find_all("div", class_="listagem-posts-conteudos")

    for element in course_page_elements:
        course_title: str = (
            element.find("h3", class_="listagem-posts-titulo").text.strip() or ""
        )
        course_modalities = element.find_all("span", class_="term-lista-tipo")
        modalities = []
        for modality in course_modalities:
            text = modality.text.strip()
            modalities.append(text)
        course_url = generate_course_url(course_title)

    return courses


def generate_course_url(title: str, base_url="https://www.cps.sp.gov.br/etec") -> str:
    normalized_title = normalize_course_name(title)
    return f"{base_url}/{normalized_title}"


def normalize_course_name(course_name: str) -> str:
    normalized = course_name.lower()
    normalized = unicodedata.normalize("NFD", normalized)
    normalized = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )

    normalized = re.sub(r"[^\w\s-]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    normalized = normalized.replace(" ", "-")
    normalized = re.sub(r"-+", "-", normalized)
    normalized = normalized.strip("-")

    return normalized


def main():
    page = make_requests(
        "https://www.cps.sp.gov.br/etec/cursos-oferecidos-pelas-etecs/"
    )
    content = parse_page(page)
    print(content)


if __name__ == "__main__":
    main()
