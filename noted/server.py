from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

from noted.recipe import RecipeManager


## UI Theme
THEME = {"largeText": 24}


class ResultBody(BaseModel):
    verdict: str


def create_server(manager: RecipeManager):
    ## Setup the server
    app = FastAPI()

    app.mount(
        "/assets",
        StaticFiles(directory="static/assets", html=True),
        name="static",
    )

    ## Development setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", response_class=HTMLResponse)
    def read_root(request: Request):
        return FileResponse(
            "static/index.html",
        )

    @app.get("/app/config", response_class=JSONResponse)
    def app_config():
        config = manager.config()
        return config

    @app.get("/task/current", response_class=JSONResponse)
    def task_current():
        task = manager.current()
        return task

    @app.post("/task/advance", response_class=JSONResponse)
    def task_advance(result: ResultBody):
        manager.result(result)
        manager.advance()
        return {"message": "OK"}

    return app
