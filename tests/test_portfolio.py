import json
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.models.projects import ArcGISMap, Project
from app.paths import BASE_DIR
from app.project_data import load_projects
from app.routes.Init import user
from main import app, templates


class PageElements(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.elements: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.elements.append((tag, dict(attrs)))


class PortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.project = user.projects[0]

    def test_routes_and_static_images(self) -> None:
        for path in ["/", "/portfolio", *[f"/portfolio/{p.slug}" for p in user.projects]]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertNotIn("<iframe", response.text)
        for project in user.projects:
            self.assertIn(f"/portfolio/{project.slug}", self.client.get("/portfolio").text)
            for component in project.components:
                self.assertEqual(self.client.get(component.url).status_code, 200)
        self.assertEqual(self.client.get("/static/css/styles.css").status_code, 200)
        self.assertEqual(self.client.get("/portfolio/unknown-project").status_code, 404)

    def test_embed_is_optional_and_rendered_with_fallback(self) -> None:
        project = Project.model_validate({
            **self.project.model_dump(),
            "arcgis_map": None,
            "embed_url": "https://www.arcgis.com/apps/mapviewer/index.html?webmap=test&mode=view",
        })
        with patch.object(user, "projects", [project]):
            detail = self.client.get(f"/portfolio/{project.slug}").text
            self.assertIn('<iframe src="https://www.arcgis.com/', detail)
            self.assertIn("&amp;mode=view", detail)
            self.assertIn('title="Interactive map:', detail)
            self.assertIn('loading="lazy"', detail)
            self.assertIn("Open interactive map", detail)
            self.assertIn("Map gallery", detail)
            self.assertNotIn("<iframe", self.client.get("/").text)
            self.assertNotIn("<iframe", self.client.get("/portfolio").text)
            self.assertNotIn("js.arcgis.com", detail)

    def test_arcgis_component_and_script_are_scoped_to_project(self) -> None:
        detail = self.client.get("/portfolio/disneyland-energy-conservation").text
        parser = PageElements()
        parser.feed(detail)
        maps = [attrs for tag, attrs in parser.elements if tag == "arcgis-embedded-map"]
        self.assertEqual(len(maps), 1)
        expected = {
            "item-id": "7997e897da4d472290638160c061c6b4",
            "portal-url": "https://pcc-gis.maps.arcgis.com/",
            "theme": "light",
            "center": "-117.92005139702917,33.81127780256998",
            "scale": "18055.954822",
        }
        for name, value in expected.items():
            self.assertEqual(maps[0][name], value)
        for name in ["bookmarks", "heading", "legend", "information", "time-zone-label"]:
            self.assertIn(f"{name}-enabled", maps[0])
        self.assertNotIn("scroll-enabled", maps[0])
        scripts = [attrs for tag, attrs in parser.elements if tag == "script" and "js.arcgis.com" in (attrs.get("src") or "")]
        self.assertEqual(scripts, [{"type": "module", "src": "https://js.arcgis.com/5.1/embeddable-components/"}])
        self.assertLess(detail.index(scripts[0]["src"] or ""), detail.index("</head>"))
        self.assertIn('href="https://pcc-gis.maps.arcgis.com/apps/mapviewer/index.html?webmap=7997e897da4d472290638160c061c6b4"', detail)
        self.assertLess(detail.index("<arcgis-embedded-map"), detail.index('class="project-gallery"'))
        self.assertIn("/static/images/projects/disneyland-energy-conservation/energy-conservation-map.png", detail)
        for path in ["/", "/portfolio", "/portfolio/orange-county-water-quality"]:
            with self.subTest(path=path):
                page = self.client.get(path).text
                self.assertNotIn("js.arcgis.com", page)
                self.assertNotIn("<arcgis-embedded-map", page)

    def test_interactive_showcase_and_detail_flow(self) -> None:
        for path in ["/", "/portfolio"]:
            with self.subTest(path=path):
                page = self.client.get(path).text
                self.assertIn("Explore interactive map", page)
                self.assertIn("project-kind-interactive", page)
                self.assertNotIn("js.arcgis.com", page)
        homepage = self.client.get("/").text
        self.assertIn("/portfolio/disneyland-energy-conservation#interactive-map", homepage)
        detail = self.client.get("/portfolio/disneyland-energy-conservation").text
        self.assertLess(detail.index("<arcgis-embedded-map"), detail.index('class="project-narrative"'))
        self.assertLess(detail.index('class="project-narrative"'), detail.index('class="project-gallery"'))
        self.assertIn('href="#project-images"', detail)

    def test_static_galleries_use_real_project_images(self) -> None:
        population = next(project for project in user.projects if project.slug == "lower-48-population")
        page = self.client.get(f"/portfolio/{population.slug}").text
        parser = PageElements()
        parser.feed(page)
        images = [attrs for tag, attrs in parser.elements if tag == "img" and str(attrs.get("src", "")).startswith("/static/images/projects/")]
        self.assertEqual(len(images), 3)
        self.assertEqual(len({attrs["src"] for attrs in images}), 3)
        self.assertTrue(all(attrs.get("alt") for attrs in images))
        self.assertNotIn("project-kind-interactive", page)
        for project in user.projects:
            with self.subTest(slug=project.slug):
                parser = PageElements()
                parser.feed(self.client.get(f"/portfolio/{project.slug}").text)
                image_sources = [attrs.get("src", "") for tag, attrs in parser.elements if tag == "img"]
                self.assertIn(project.thumbnail.url, image_sources)
                self.assertTrue(all(component.url.startswith(f"/static/images/projects/{project.slug}/") for component in project.components))
                self.assertNotIn("placeholder", project.thumbnail.name.lower())

    def test_arcgis_validation_and_exclusive_embed_formats(self) -> None:
        self.assertIsNotNone(self.project.arcgis_map)
        assert self.project.arcgis_map is not None
        original = self.project.arcgis_map.model_dump(mode="json")
        invalid_changes: list[dict[str, object]] = [
            {"item_id": "not-an-id"}, {"item_id": "g" * 32},
            {"center": [181, 0]}, {"center": [0, -91]}, {"center": [0]},
            {"center": [float("nan"), 0]}, {"scale": 0}, {"scale": -1},
            {"scale": float("inf")}, {"theme": "purple"}, {"html": "<script></script>"},
        ]
        for url in [
            "http://pcc-gis.maps.arcgis.com", "https://pcc-gis.maps.arcgis.com.evil.example",
            "https://unapproved.maps.arcgis.com", "https://user:pass@pcc-gis.maps.arcgis.com",
            "https://pcc-gis.maps.arcgis.com:8443", "https://pcc-gis.maps.arcgis.com/path",
            "https://pcc-gis.maps.arcgis.com?token=test", "https://pcc-gis.maps.arcgis.com#fragment",
        ]:
            invalid_changes.append({"portal_url": url})
        for changes in invalid_changes:
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                ArcGISMap.model_validate({**original, **changes})
        with self.assertRaisesRegex(ValidationError, "either embed_url or arcgis_map"):
            Project.model_validate({
                **self.project.model_dump(), "embed_url": "https://www.arcgis.com/apps/mapviewer/",
            })
        for center in [[-180, -90], [180, 90]]:
            ArcGISMap.model_validate({**original, "center": center})

    def test_arcgis_disabled_options_are_omitted(self) -> None:
        assert self.project.arcgis_map is not None
        options = {
            name: False for name in ["bookmarks_enabled", "heading_enabled", "legend_enabled",
                                    "information_enabled", "scroll_enabled", "time_zone_label_enabled"]
        }
        project = Project.model_validate({
            **self.project.model_dump(),
            "arcgis_map": {**self.project.arcgis_map.model_dump(), **options},
        })
        with patch.object(user, "projects", [project]):
            parser = PageElements()
            parser.feed(self.client.get(f"/portfolio/{project.slug}").text)
            attributes = next(attrs for tag, attrs in parser.elements if tag == "arcgis-embedded-map")
            for name in options:
                self.assertNotIn(name.replace("_", "-"), attributes)

    def test_rejects_untrusted_embed_urls(self) -> None:
        for url in [
            "http://www.arcgis.com/map", "javascript:alert(1)",
            "https://www.arcgis.com.evil.example/map", "https://evil.example/map",
            "https://user:password@www.arcgis.com/map", "https://www.arcgis.com:8443/map",
        ]:
            with self.subTest(url=url), self.assertRaises(ValidationError):
                Project.model_validate({**self.project.model_dump(), "embed_url": url})

    def test_empty_and_single_featured_states(self) -> None:
        with patch.object(user, "projects", []):
            self.assertIn("Projects will be added soon", self.client.get("/").text)
            self.assertIn("Projects will be added soon", self.client.get("/portfolio").text)
            self.assertNotIn('id="projectHighlights"', self.client.get("/").text)
        with patch.object(user, "projects", [self.project]):
            self.assertNotIn('data-bs-slide="next"', self.client.get("/").text)
        unfeatured = Project.model_validate({**self.project.model_dump(), "featured": False})
        with patch.object(user, "projects", [unfeatured]):
            self.assertNotIn('id="projectHighlights"', self.client.get("/").text)
            self.assertIn(unfeatured.title, self.client.get("/").text)

    def test_content_validation(self) -> None:
        original = self.project.model_dump(mode="json")
        invalid_changes: list[dict[str, object]] = [
            {"slug": "Bad Slug"}, {"title": " "}, {"summary": ""}, {"components": []},
        ]
        for changes in invalid_changes:
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                Project.model_validate({**original, **changes})
        with TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps([original, original]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unique"):
                load_projects(path)
            for url in ["/static/images/missing.png", "/static/images/../../main.py"]:
                with self.subTest(url=url):
                    path.write_text(json.dumps([{
                        **original,
                        "components": [{"name": "Test", "url": url, "desc": ""}],
                    }]), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "Invalid image"):
                        load_projects(path)
            path.write_text("not json", encoding="utf-8")
            with self.assertRaises(ValidationError):
                load_projects(path)

    def test_description_is_escaped_and_paragraphs_render(self) -> None:
        project = Project.model_validate({
            **self.project.model_dump(), "desc": "<script>alert(1)</script>\n\nSecond paragraph",
        })
        with patch.object(user, "projects", [project]):
            detail = self.client.get(f"/portfolio/{project.slug}").text
            self.assertNotIn("<script>alert(1)</script>", detail)
            self.assertIn("&lt;script&gt;", detail)
            self.assertIn("<p>Second paragraph</p>", detail)

    def test_templates_have_no_missing_fields(self) -> None:
        from jinja2 import StrictUndefined

        with patch.object(templates.env, "undefined", StrictUndefined):
            for path in ["/", "/portfolio", f"/portfolio/{self.project.slug}"]:
                self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(len(load_projects(BASE_DIR / "data" / "projects.json")), len(user.projects))

    def test_contact_options_exclude_phone_on_every_page(self) -> None:
        for path in ["/", "/portfolio", *[f"/portfolio/{p.slug}" for p in user.projects]]:
            with self.subTest(path=path):
                page = self.client.get(path).text
                parser = PageElements()
                parser.feed(page)
                links = [attrs.get("href", "") or "" for tag, attrs in parser.elements if tag == "a"]
                self.assertFalse(any(link.startswith("tel:") for link in links))
                self.assertNotIn("3238057622", "".join(character for character in page if character.isdigit()))
                self.assertNotIn("Call Me", page)
                self.assertIn(f"mailto:{user.email}", links)
                self.assertTrue(any(link.startswith("https://www.linkedin.com/in/") for link in links))


if __name__ == "__main__":
    unittest.main()
