import requests
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


def main():
    page = make_requests(
        "https://www.cps.sp.gov.br/etec/cursos-oferecidos-pelas-etecs/"
    )
    content = parse_page(page)
    print(content)


if __name__ == "__main__":
    main()
