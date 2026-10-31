from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator
from app.models.component import Component

# Add an exact hostname here when using a different trusted map provider.
EMBED_HOSTS = frozenset({
    "arcgis.com", "www.arcgis.com", "storymaps.arcgis.com", "experience.arcgis.com",
})
ARCGIS_PORTAL_HOSTS = frozenset({
    "arcgis.com", "www.arcgis.com", "pcc-gis.maps.arcgis.com",
})


class ArcGISMap(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid", allow_inf_nan=False)

    item_id: str = Field(pattern=r"^[a-fA-F0-9]{32}$")
    portal_url: HttpUrl
    center: tuple[float, float]
    scale: float = Field(gt=0)
    theme: Literal["light", "dark"] = "light"
    bookmarks_enabled: bool = False
    heading_enabled: bool = False
    legend_enabled: bool = False
    information_enabled: bool = False
    scroll_enabled: bool = False
    time_zone_label_enabled: bool = False

    @field_validator("portal_url")
    @classmethod
    def validate_portal_url(cls, value: HttpUrl) -> HttpUrl:
        if (
            value.scheme != "https"
            or value.host not in ARCGIS_PORTAL_HOSTS
            or value.username is not None
            or value.password is not None
            or value.port != 443
            or value.path not in (None, "/")
            or value.query is not None
            or value.fragment is not None
        ):
            raise ValueError("Portal URL must be an approved HTTPS portal origin without credentials, a custom port, or a path")
        return value

    @field_validator("center")
    @classmethod
    def validate_center(cls, value: tuple[float, float]) -> tuple[float, float]:
        longitude, latitude = value
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            raise ValueError("Map center must be a longitude/latitude pair within geographic bounds")
        return value

    @property
    def viewer_url(self) -> str:
        return f"{str(self.portal_url).rstrip('/')}/apps/mapviewer/index.html?webmap={self.item_id}"


class Project(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    desc: str = Field(min_length=1)
    components: list[Component] = Field(min_length=1)
    featured: bool = False
    embed_url: HttpUrl | None = None
    arcgis_map: ArcGISMap | None = None

    @model_validator(mode="after")
    def validate_embed_format(self) -> Self:
        if self.embed_url is not None and self.arcgis_map is not None:
            raise ValueError("Choose either embed_url or arcgis_map, not both")
        return self

    @property
    def interactive_map_url(self) -> str | None:
        if self.arcgis_map is not None:
            return self.arcgis_map.viewer_url
        return str(self.embed_url) if self.embed_url is not None else None

    @field_validator("embed_url")
    @classmethod
    def validate_embed_url(cls, value: HttpUrl | None) -> HttpUrl | None:
        if value is not None and (
            value.scheme != "https"
            or value.host not in EMBED_HOSTS
            or value.username is not None
            or value.password is not None
            or value.port != 443
        ):
            raise ValueError("Embed URL must use HTTPS on an approved map host without credentials or a custom port")
        return value

    @property
    def thumbnail(self) -> Component:
        return self.components[0]

    @property
    def paragraphs(self) -> list[str]:
        return [paragraph.strip() for paragraph in self.desc.split("\n\n") if paragraph.strip()]
