"""This module implements the behaviour of the endpoints of the API"""
import os
import io
import copy
from urllib import response
from urllib import request
import PIL
from PIL import Image
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel, ValidationError, validator
from src.models.model import Model
from src.api.services import do_predict, do_upload, evaluate_classification

# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

# from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from time import time


from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary,
    push_to_gateway,
    CollectorRegistry,
    generate_latest,
)


path_saved_model = os.path.join("models", "saved-model-optimal")

## remove the parameter cur_path if appears the error "No such file 'params.yaml'"
model = Model()
model = model.loadModel(path_saved_model)


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=[
            "http://0.0.0.0:9200",
            "http://0.0.0.0:9300",
            "http://localhost:9200",
            "http://localhost:9300",
            "http://archinet-se4ai.ddns.net:9200",
            "http://archinet-se4ai.ddns.net:9200/",
        ],
        allow_methods=["GET", "PUT", "POST", "OPTIONS"],
        allow_headers=["*"],
        allow_credentials=True,
    )
]
app = FastAPI(middleware=middleware)


REQUEST_TIME = Gauge(
    "request_processing_seconds",
    "Time spent processing request",
    ["method", "endpoint"],
)

dummy_hist = Histogram("myhist", "desc_hist", buckets=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
dummy_summary = Summary("mySummary", "desc_shummary")


counter_predictions = Counter(
    "counter_predictions",
    "Counter for predictions that have been made",
)
counter_labeled_images = Counter(
    "counter_labeled_images",
    "Counter for images sent to extend the dataset",
)
counter_feedback = Counter(
    "counter_feedback",
    "Counter for feedbacks sent by the experts",
)


class ImageValidator(BaseModel):
    """Pydantic validator for images"""

    # Same name as parameter of body request
    image: UploadFile

    @validator("image")
    def check_image(cls, image):
        """Checks that the input file is actually an image"""
        img = image.file.read()
        try:
            Image.open(io.BytesIO(img))
            image.file.close()
        except PIL.UnidentifiedImageError as exc:
            raise ValueError(
                "Image upload error, the file provided is not an image."
            ) from exc
        return img


class LabelValidator(BaseModel):
    """Pydantic validator for class labels"""

    val: int

    @validator("val")
    def check_val(cls, value):
        """Checks that the provided label is between 0 and 9"""
        if not 0 <= value < 10:
            raise ValueError(
                "Id label error, the label must be a value between 0 and 9."
            )


# @app.get("/metrics")
# def get_metrics():
#    return generate_latest(REGISTRY)


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)


@app.post("/extend_dataset/")
async def upload_file(imgfile: UploadFile, label: int):
    """Upload an image in order to expand the dataset"""
    try:
        LabelValidator(val=label)
        ImageValidator(image=copy.deepcopy(imgfile))
        start = time()
        res = await do_upload(imgfile, label)
        end = time()
        counter_labeled_images.inc()
        REQUEST_TIME.labels("POST", "/extend_dataset").set(end - start)
        return res
    except ValidationError as exc:
        raise HTTPException(status_code=406, detail=str(exc.raw_errors[0].exc)) from exc


@app.post("/classify_image/")
async def predict(imgfile: UploadFile):
    """Use the ml model in order to classify an image"""
    try:

        ImageValidator(image=copy.deepcopy(imgfile))
        start = time()
        res = await do_predict(imgfile, model)
        end = time()
        REQUEST_TIME.labels("POST", "/classify_image").set(end - start)
        counter_predictions.inc()
        return res
    except ValidationError as exc:
        raise HTTPException(status_code=406, detail=str(exc.raw_errors[0].exc)) from exc


@app.put("/feedback_class/")
async def eval_class(id_img: int, new_class: int):
    """Allows experts to give the real label of an image already classified"""
    dummy_hist.observe(100)
    dummy_summary.observe(512)
    try:
        LabelValidator(val=new_class)
        start = time()
        res = evaluate_classification(id_img, new_class)
        end = time()
        REQUEST_TIME.labels("POST", "/feedback_class").set(end - start)
        if res == "ko404":
            raise HTTPException(
                status_code=404, detail="There is no classified image with that id."
            )
        if res == "ko406":
            raise HTTPException(
                status_code=406,
                detail="There is already a class specified for that that image id.",
            )
        counter_feedback.inc()
        return res
    except ValidationError as exc:
        raise HTTPException(status_code=406, detail=str(exc.raw_errors[0].exc)) from exc
