from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.staticfiles import StaticFiles
from app.routes.Init import user, images

app = FastAPI()

# HTML templates
templates = Jinja2Templates(directory="templates")
# css, javascript, images, etc
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
    )

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="index.html",
        context={
            "user":user,
            "images":images
        }
    )
