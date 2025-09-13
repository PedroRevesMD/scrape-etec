import re
import unicodedata
from bs4 import BeautifulSoup

BASE_URL = "https://www.cps.sp.gov.br/cursos-etec"
HTML_PARSER = "html.parser"


def generate_course_url(title: str, base_url=BASE_URL) -> str:
    normalized_title = normalize_course_name(title)
    return f"{base_url}/{normalized_title}"


def normalize_course_name(name: str) -> str:
    course_name = name.lower()
    course_name = _remove_accents(course_name)
    course_name = _clean_special_chars(course_name)
    course_name = _normalize_spaces(course_name)
    course_name = _convert_to_url(course_name)

    return course_name


def _clean_special_chars(text: str) -> str:
    return re.sub(r"[^\w\s-]", "", text)


def _remove_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def _normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _convert_to_url(text: str) -> str:
    text = text.replace(" ", "-")
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def remove_schools_duplicates(schools: list[str]) -> list[str]:
    return list(set(schools))


def parse_page(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, HTML_PARSER)
