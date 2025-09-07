import re
import unicodedata


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
