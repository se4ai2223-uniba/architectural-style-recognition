from fastapi import FastAPI, HTTPException
from src.models.model import Model
from classify import *
from eval_class import *
import shutil
from typing import Union


path_saved_model = os.path.join("..", "..", "models", "saved-model-optimal")

## remove the parameter cur_path if appears the error "No such file 'params.yaml'"
model = Model(cur_path=os.path.join("..", ".."))

model = model.loadModel(path_saved_model)


app = FastAPI()


@app.post("/uploadfile/")
async def upload_file(file: UploadFile, label: int):

    # controllare che label sia nel giusto range e decidere se debba essere testuale o numerica
    try:
        contents = await file.read()
        new_id = read_id()
        image_path = os.path.join(
            "..", "..", "data", "external", "images", str(new_id) + "_" + file.filename
        )
        with open(image_path, "wb") as f:
            await f.write(contents)
        print("File Uploaded")

        insert_into_csv(
            os.path.join("..", "..", "data", "external", "dataset.csv"),
            str(new_id),
            str(label),
        )
        increase_id()
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        file.file.close()
        return {"filename": file.filename, "label": label}


@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        res = await do_predict(file, model)
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
    return res

@app.post("/eval_class/")
async def eval_class(id_img: int, new_class: int):
    try:
        res = evaluate_classification(id_img, new_class)   
    except:
        raise HTTPException(status_code=500, detail="Internal server error") 
    if(res == 'ko404'):
        raise HTTPException(status_code=404, detail="There is no classified image with that id")
    if(res == 'ko406'):
        raise HTTPException(status_code=406, detail="There is already a class specified for that that image id")
    
    return res
