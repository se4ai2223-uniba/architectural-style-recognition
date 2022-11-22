from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, ValidationError, validator
from src.models.model import Model
from classify import *
from eval_class import *
from upfile import *
import cv2
import json
import PIL
from PIL import Image
import io
path_saved_model = os.path.join("..", "..", "models", "saved-model-optimal")

## remove the parameter cur_path if appears the error "No such file 'params.yaml'"
model = Model(cur_path=os.path.join("..", ".."))
model = model.loadModel(path_saved_model)
app = FastAPI()


class PredictPayload(BaseModel):

    # Same name as parameter of body request
    maybeImage: UploadFile = File(...)

    @validator("*")
    def is_image(cls, v):
        contents = v.file.read()
        try:
            Image.open(io.BytesIO(contents))
        except PIL.UnidentifiedImageError:
            return "Image needed!"

        return contents

class LabelModel(BaseModel):
    val: int

@app.post("/uploadfile/")
async def upload_file(file: UploadFile, label: int):
    try:
        labelModel = LabelModel(
        val = label
        )
        res = await do_upload(file, label)
        return res    
    except ValidationError as e:
        raise HTTPException(status_code=406, detail=str(e.raw_errors[0].exc))

@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        img = PredictPayload(
            maybeImage = file
        )
        res = await do_predict(file, model)
        return res
    except ValidationError as e:
        raise HTTPException(status_code=406, detail=str(e.raw_errors[0].exc))


@app.post("/eval_class/")
async def eval_class(id_img: int, new_class: int):
    res = evaluate_classification(id_img, new_class)   
    if(res == 'ko404'):
        raise HTTPException(status_code=404, detail="There is no classified image with that id")
    if(res == 'ko406'):
        raise HTTPException(status_code=406, detail="There is already a class specified for that that image id")    
    return res