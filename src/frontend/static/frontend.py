import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

#uvicorn src.frontend.static.frontend:app --reload --host 0.0.0.0 --port 82
app = FastAPI()
path_to_static = os.path.join('src', 'frontend', 'static')
app.mount("/static", StaticFiles(directory=path_to_static), name="static")