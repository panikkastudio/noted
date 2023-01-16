from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from noted.recipe import RecipeManager


## UI Theme
THEME = {"largeText": 24}


def get_task_view(env: Jinja2Templates, config: dict):
    COMPONENT_RENDERER = lambda type: "{% include 'components/" + type + ".html' %}"
    view_type = config.get("view_type")

    if "text" == view_type:
        component = COMPONENT_RENDERER(view_type)
        return env.from_string(component)

    if "html" == view_type:
        template_raw = config.get("html_template")
        return env.from_string(template_raw)

    if "ner" == view_type:
        component = COMPONENT_RENDERER("ner")
        return env.from_string(component)

    if "ner_manual" == view_type:
        component = COMPONENT_RENDERER("ner_manual")
        return env.from_string(component)

    if "classification" == view_type:
        component = COMPONENT_RENDERER("classification")
        return env.from_string(component)


def create_server(manager: RecipeManager):
    ## Setup the server
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="assets/static"), name="static")
    templates = Jinja2Templates(directory="assets/templates")

    ## Development setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ## Setup UI templating
    config = manager.config()
    template = get_task_view(templates.env, config)

    @app.get("/", response_class=HTMLResponse)
    def read_root(request: Request):
        task = manager.current()
        return templates.TemplateResponse(
            "index.html",
            {
                "task": task,
                "request": request,
                "template": template.render(**task, **config),
            },
        )

    @app.post("/task/advance", response_class=JSONResponse)
    def task_advance(request: Request):
        print(request.body)
        manager.result(request.body)

        manager.advance()
        return {"message": "OK"}

    return app
