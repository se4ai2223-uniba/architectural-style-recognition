from fastapi import FastAPI
app = FastAPI()


from classify import *
from eval_class import * 


@app.post("/uploadimage/")
async def create_upload_image(file: UploadFile):
    return await upload_img(file)


@app.post("/eval_class/")
async def eval_class( id_img: int, new_class: str):
    res = evaluate_classification(id_img, new_class)
    return {"result": res}
