from pydantic import BaseModel, ConfigDict, Field


class Component(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1)
    url: str = Field(pattern=r"^/static/images/[^?#]+$")
    desc: str
