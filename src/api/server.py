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
from fastapi.staticfiles import StaticFiles


# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

# from fastapi.middleware.cors import CORSMiddleware


path_saved_model = os.path.join("models", "saved-model-optimal")

## remove the parameter cur_path if appears the error "No such file 'params.yaml'"
model = Model()
model = model.loadModel(path_saved_model)


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=[
            "http://0.0.0.0:9200",
            "http://archinet-se4ai.ddns.net:9200",
            "http://archinet-se4ai.ddns.net:9200/",
        ],
        allow_methods=["GET", "PUT", "POST", "OPTIONS"],
        allow_headers=["*"],
        allow_credentials=True,
    )
]


app = FastAPI(middleware=middleware)


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



# app.add_middleware(
#    CORSMiddleware,
#    allow_origins=[
#        "http://0.0.0.0:9200",
#        "http://0.0.0.0:9200/",
#        "http://0.0.0.0:9200/static/index.html",
#        "http://0.0.0.0:9200/static/expert-add-script.js",
#        "http://0.0.0.0:9200/static/expert-form-script.js",
#        "http://archinet-se4ai.ddns.net:9200",
#        "http://archinet-se4ai.ddns.net:9200/",
#        "http://archinet-se4ai.ddns.net:9200/static/index.html",
#        "http://archinet-se4ai.ddns.net:9200/static/expert-add-script.js",
#        "http://archinet-se4ai.ddns.net:9200/static/expert-form-script.js",
#    ],
#    allow_methods=["*"],
#    allow_headers=["*"],
#    allow_credentials=True,
# )


@app.post("/extend_dataset/")
async def upload_file(imgfile: UploadFile, label: int):
    """Upload an image in order to expand the dataset"""
    try:
        LabelValidator(val=label)
        ImageValidator(image=copy.deepcopy(imgfile))
        res = await do_upload(imgfile, label)
        return res
    except ValidationError as exc:
        raise HTTPException(status_code=406, detail=str(exc.raw_errors[0].exc)) from exc


@app.post("/classify_image/")
async def predict(imgfile: UploadFile):
    """Use the ml model in order to classify an image"""
    try:
        ImageValidator(image=copy.deepcopy(imgfile))
        res = await do_predict(imgfile, model)
        return res
    except ValidationError as exc:
        raise HTTPException(status_code=406, detail=str(exc.raw_errors[0].exc)) from exc


@app.put("/feedback_class/")
async def eval_class(id_img: int, new_class: int):
    """Allows experts to give the real label of an image already classified"""
    try:
        LabelValidator(val=new_class)
        res = evaluate_classification(id_img, new_class)
        if res == "ko404":
            raise HTTPException(
                status_code=404, detail="There is no classified image with that id."
            )
        if res == "ko406":
            raise HTTPException(
                status_code=406,
                detail="There is already a class specified for that that image id.",
            )
        return res
    except ValidationError as exc:
        raise HTTPException(status_code=406, detail=str(exc.raw_errors[0].exc)) from exc
