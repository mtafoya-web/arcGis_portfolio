from pydantic import BaseModel, EmailStr, Field
from app.models.projects import Project

class User(BaseModel):
    name: str
    email: EmailStr
    bio: str
    about:list[str]
    projects: list[Project] = Field(default_factory=list)
