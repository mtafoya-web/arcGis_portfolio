from pydantic import BaseModel
from app.models.component import Component

class Project(BaseModel):
    title: str
    desc: str
    components: list[Component]
