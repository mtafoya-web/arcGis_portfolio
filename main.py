from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.paths import BASE_DIR
from app.routes.Init import user

app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user,
            "featured_projects": [project for project in user.projects if project.featured][:3],
            "selected_projects": user.projects[:6],
        },
    )


@app.get("/portfolio", response_class=HTMLResponse)
def portfolio(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="portfolio.html", context={"user": user},
    )


@app.get("/portfolio/{slug}", response_class=HTMLResponse)
def project_detail(request: Request, slug: str) -> HTMLResponse:
    project = next((project for project in user.projects if project.slug == slug), None)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse(
        request=request, name="project.html", context={"user": user, "project": project},
    )
