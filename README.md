# ArcGIS Portfolio

Portfolio website for Samantha Galaviz Archila, focused on ArcGIS, web mapping, conservation, wildlife, and environmental project work.

The project is a Python FastAPI application that renders Jinja2 templates and serves static assets for styling and images. The current home page includes a hero section, about section, highlighted project carousel, latest work grid, contact bar, and footer.

## Tech Stack

- Python
- FastAPI
- Jinja2 templates
- Pydantic models
- Bootstrap 5.3.3
- Font Awesome
- Custom CSS

## Project Structure

```text
.
|-- main.py
|-- app/
|   |-- models/
|   |   |-- component.py
|   |   |-- projects.py
|   |   `-- user.py
|   `-- routes/
|       `-- Init.py
|-- static/
|   |-- css/
|   |   `-- styles.css
|   `-- images/
|       |-- hero_bg.png
|       |-- otter_sprite.png
|       `-- profile.png
`-- templates/
    |-- base.html
    `-- index.html
```

## Current Pages

| Page | Route | Status | Notes |
| --- | --- | --- | --- |
| Home | `/` | Implemented | Uses `templates/index.html` with shared layout from `templates/base.html`. |
| About Me | `/about` | Planned | Navbar link exists, but the route and template still need to be added. |
| Portfolio | `/portfolio` | Planned | Navbar link exists, but the route, template, and project components still need to be added. |
| Resume | `/resume` | Planned | Navbar link exists, but the route and template still need to be added. |

## Local Setup

1. Create and activate a virtual environment.

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install fastapi uvicorn jinja2 pydantic email-validator
   ```

3. Run the development server.

   ```powershell
   uvicorn main:app --reload
   ```

4. Open the site.

   ```text
   http://127.0.0.1:8000
   ```

## Data Model

The application keeps portfolio data in Pydantic models:

- `User`: profile information, bio, about paragraphs, and projects.
- `Project`: project title, description, and associated components.
- `Component`: reusable project/component item with a name, URL, and description.

Initial content is loaded in `app/routes/Init.py`.
![Website models and relationships](static/images/models.png)

## Development Notes

- Shared layout, navigation, contact section, footer, external CSS/JS links, and template blocks live in `templates/base.html`.
- The home page content lives in `templates/index.html`.
- Main styling lives in `static/css/styles.css`.
- Static images are served from `static/images/`.
- New pages should extend `templates/base.html` and define their own `{% block title %}` and `{% block content %}` sections.

## GitHub Pull Request Workflow

When this project is pushed to GitHub, create a separate pull request for each page that needs components added to it. This keeps review focused and makes it easier to test each page independently.

Recommended PR breakdown:

- `about-page-components`: add the `/about` route, template, and About Me page components.
- `portfolio-page-components`: add the `/portfolio` route, template, project data, and portfolio component layout.
- `resume-page-components`: add the `/resume` route, template, resume content, and downloadable resume link if needed.

Each page PR should include:

- The FastAPI route for the page.
- The Jinja2 template for the page.
- Any new reusable models or component data needed by the page.
- Any required CSS updates.
- A short manual test note confirming the page loads locally.

## Next Work

- Add `/about`, `/portfolio`, and `/resume` routes.
- Add matching templates for planned pages.
- Replace placeholder project names, descriptions, and images with final portfolio content.
- Move repeated project card/carousel markup into reusable template partials if the pages begin sharing the same component patterns.
