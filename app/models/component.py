from pydantic import BaseModel


class Component(BaseModel):
    name: str
    url: str
    desc: str