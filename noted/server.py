from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

from noted.recipe import RecipeManager
from ._internal.path import get_library_dir

## UI Theme
THEME = {"largeText": 24}


def create_server(manager: RecipeManager):
    ## Setup the server
    app = FastAPI()

    static_dir = f"{get_library_dir()}/_static"
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="static")

    ## Development setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", response_class=HTMLResponse)
    def read_root(request: Request):
        return FileResponse(f"{static_dir}/index.html")

    @app.get("/app/config", response_class=JSONResponse)
    def app_config():
        config = manager.config()
        return config

    @app.get("/task/current", response_class=JSONResponse)
    def task_current():
        task = manager.current()
        return task

    @app.post("/task/advance", response_class=JSONResponse)
    async def task_advance(request: Request):
        result = await request.json()
        manager.result(result)
        manager.advance()
        return {"message": "OK"}

    return app
