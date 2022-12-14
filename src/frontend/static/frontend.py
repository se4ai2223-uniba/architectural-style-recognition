import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

#uvicorn src.frontend.static.frontend:app --reload --host 0.0.0.0 --port 82
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path_to_static = os.path.join('src', 'frontend', 'static')
app.mount("/static", StaticFiles(directory=path_to_static), name="static")