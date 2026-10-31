from pathlib import Path

from pydantic import TypeAdapter

from app.models.projects import Project
from app.paths import BASE_DIR


def load_projects(path: Path = BASE_DIR / "data" / "projects.json") -> list[Project]:
    projects = TypeAdapter(list[Project]).validate_json(path.read_text(encoding="utf-8"))
    slugs = [project.slug for project in projects]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Project slugs must be unique")
    image_root = (BASE_DIR / "static" / "images").resolve()
    for project in projects:
        for component in project.components:
            image = (BASE_DIR / component.url.lstrip("/")).resolve()
            if not image.is_relative_to(image_root) or not image.is_file():
                raise ValueError(f"Invalid image for project '{project.slug}': {component.url}")
    return projects
