from fastapi import FastAPI
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
async def create_upload_file(file: UploadFile, label: str):

    # conteollare che label sia nel giusto range e decidere se debba essere testuale o numerica
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
        print("FastAPI: Exception thrown in uploadimage endpoint")
    finally:
        file.file.close()
        return {"filename": file.filename, "Label": label}


@app.post("/predict/")
async def predict(file: UploadFile):
    return await do_predict(file, model)


# creare endpoint per classificazione


@app.post("/eval_class/")
async def eval_class(id_img: int, new_class: str):
    res = evaluate_classification(id_img, new_class)
    return {"result": res}
