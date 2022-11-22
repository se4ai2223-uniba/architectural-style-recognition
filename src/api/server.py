from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from src.models.model import Model
from classify import *
from eval_class import *
from upfile import *
import cv2
path_saved_model = os.path.join("..", "..", "models", "saved-model-optimal")

## remove the parameter cur_path if appears the error "No such file 'params.yaml'"
model = Model(cur_path=os.path.join("..", ".."))
model = model.loadModel(path_saved_model)
app = FastAPI()


class ImageModel(BaseModel):
    image: UploadFile
    @validator('image')
    def check_image(cls, image):
        try:
            img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        except:
            raise ValueError('File is not an image')

class LabelModel(BaseModel):
    val: int
    @validator('val')
    def check_val(cls, v):
        if not (v >= 0 and v < 10):
            raise ValueError('Mamt!')

@app.post("/uploadfile/")
async def upload_file(file: UploadFile, label: LabelModel):
    res = await do_upload(file, label.val)
    return res

@app.post("/predict/")
async def predict(file: UploadFile):
    res = await do_predict(file, model)
    return res

@app.post("/eval_class/")
async def eval_class(id_img: int, new_class: int):
    res = evaluate_classification(id_img, new_class)   
    if(res == 'ko404'):
        raise HTTPException(status_code=404, detail="There is no classified image with that id")
    if(res == 'ko406'):
        raise HTTPException(status_code=406, detail="There is already a class specified for that that image id")    
    return res