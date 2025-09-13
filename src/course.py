from dataclasses import dataclass


@dataclass
class CourseInfo:
    title: str
    modalities: list[str]
    description: str
    workload: str
    semesters: str
    course_area: str
    requirements: str
    course_field: str
    where_to_work: str
    where_to_study: list[str]
