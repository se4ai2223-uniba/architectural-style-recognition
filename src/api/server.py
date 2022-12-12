from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, ValidationError, validator
from src.models.model import Model
from src.api.services import do_predict, do_upload, evaluate_classification
import PIL
from PIL import Image
import io
import copy
import os
from fastapi.staticfiles import StaticFiles

path_saved_model = os.path.join("models", "saved-model-optimal")

## remove the parameter cur_path if appears the error "No such file 'params.yaml'"
model = Model()
model = model.loadModel(path_saved_model)



app = FastAPI()
path_to_static = os.path.join('src', 'frontend', 'static')
app.mount("/static", StaticFiles(directory=path_to_static), name="static")

class ImageValidator(BaseModel):

    # Same name as parameter of body request
    image: UploadFile

    @validator("image")
    def checkImage(cls, image):
        img = image.file.read()
        try:
            Image.open(io.BytesIO(img))
            image.file.close()
        except PIL.UnidentifiedImageError:
            raise ValueError("Image upload error, the file provided is not an image.")
        return img


class LabelValidator(BaseModel):
    val: int

    @validator("val")
    def check_val(cls, v):
        if not (v >= 0 and v < 10):
            raise ValueError(
                "Id label error, the label must be a value between 0 and 9."
            )


@app.post("/uploadfile/")
async def upload_file(imgfile: UploadFile, label: int):
    try:
        labelModel = LabelValidator(val=label)
        img = ImageValidator(image=copy.deepcopy(imgfile))
        res = await do_upload(imgfile, label)
        return res
    except ValidationError as e:
        raise HTTPException(status_code=406, detail=str(e.raw_errors[0].exc))


@app.post("/predict/")
async def predict(imgfile: UploadFile):
    try:
        img = ImageValidator(image=copy.deepcopy(imgfile))
        res = await do_predict(imgfile, model)
        return res
    except ValidationError as e:
        raise HTTPException(status_code=406, detail=str(e.raw_errors[0].exc))


@app.put("/eval_class/")
async def eval_class(id_img: int, new_class: int):
    try:
        labelModel = LabelValidator(val=new_class)
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
    except ValidationError as e:
        raise HTTPException(status_code=406, detail=str(e.raw_errors[0].exc))
