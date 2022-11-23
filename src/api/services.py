import pandas as pd
import os
from utils import *
from fastapi import UploadFile
import numpy as np
import os

dataset_csv = os.path.join("..", "..", 'data','external','dataset.csv')
classification_csv = os.path.join("..", "..", 'data','external','predictions.csv')
dictionary_csv = os.path.join("..", "..", "data", "external", "dictionary.csv")

# riceve un'immagine e fornisce la predizione. l'immagine e la predizione vengono salvate.
async def do_predict(file: UploadFile, model):

    contents = await file.read()
    nuovo_id = read_id()
    image_path = os.path.join(
        "..", "..", "data", "external", "images", str(nuovo_id) + "_" + file.filename
    )
    with open(image_path, "wb") as f:
        f.write(contents)
    print("File Uploaded")

    preprocessed_image = prepare_image(image_path)

    predictions = model.predict(preprocessed_image)
    label = np.argmax(predictions)

    insert_into_csv(
        classification_csv,
        str(nuovo_id),
        str(label),
    )
    increase_id()
    if os.path.exists(dictionary_csv):
        df = pd.read_csv(dictionary_csv)
        label = df[str(label)][0]
        del df

    return {"filename": file.filename, "id": str(nuovo_id), "label": label}

def evaluate_classification(id, classification):
    idsd = []
    dfc = pd.read_csv(classification_csv)
    
    dfd = pd.read_csv(dataset_csv)
    if not dfc.empty:
        idsc = dfc["id_img"].to_list()

    if not dfd.empty:
        idsd = dfd["id_img"].to_list()
    
    if (id in idsc and id not in idsd): 
        insert_into_csv(
        os.path.join(dataset_csv),
        str(id),
        str(classification)
    )
        return {"result": "ok, new class saved"}
    else:
    
        if(id in idsc):
            return 'ko406' #the id exists in prediction.csv but already classified
        else:
            return 'ko404' #the id doesn't exist in prediction.csv

async def do_upload(file: UploadFile, label: int):
    contents = await file.read()
    new_id = read_id()
    image_path = os.path.join(
        "..", "..", "data", "external", "images", str(new_id) + "_" + file.filename
    )
    with open(image_path, "wb") as f:
        f.write(contents)
    print("File Uploaded")

    insert_into_csv(
        dataset_csv,
        str(new_id),
        str(label),
    )
    increase_id()  
     
    return {"filename": file.filename, "id": str(new_id), "label": label}
