'''This module implement the backend beahaviours of the APIs'''
import os
import pandas as pd
from fastapi import UploadFile
import numpy as np
from src.api.utils import *

dataset_csv = os.path.join("data", "external", "dataset.csv")
classification_csv = os.path.join("data", "external", "predictions.csv")
dictionary_csv = os.path.join("data", "external", "dictionary.csv")

# riceve un'immagine e fornisce la predizione. l'immagine e la predizione vengono salvate.
async def do_predict(file: UploadFile, model):
    '''Implement the behaviour of the predict endpoint'''

    contents = await file.read()
    nuovo_id = read_id()
    image_path = os.path.join(
        "data", "external", "images", str(nuovo_id) + "_" + file.filename
    )
    with open(image_path, "wb") as file_image:
        file_image.write(contents)
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
        data_frame = pd.read_csv(dictionary_csv)
        label = data_frame[str(label)][0]
        del data_frame

    return {"filename": file.filename, "id": str(nuovo_id), "label": label}

def evaluate_classification(id_img, classification):
    '''Implement the behaviour of the eval_class endpoint'''
    idsd = []
    idsc = []

    data_frame_class = pd.read_csv(classification_csv)


    data_frame_dataset = pd.read_csv(dataset_csv)
    if not data_frame_class.empty:
        idsc = data_frame_class["id_img"].to_list()

    if not data_frame_dataset.empty:
        idsd = data_frame_dataset["id_img"].to_list()

    if id_img in idsc and id_img not in idsd:
        insert_into_csv(os.path.join(dataset_csv), str(id_img), str(classification))
        return {"result": "ok, new class saved"}

    if id_img in idsc:
        return "ko406"  # the id exists in prediction.csv but already classified

    return "ko404"  # the id doesn't exist in prediction.csv

async def do_upload(file: UploadFile, label: int):
    '''Implement the behaviour of the uploadfile endpoint'''
    contents = await file.read()
    new_id = read_id()
    image_path = os.path.join(
        "data", "external", "images", str(new_id) + "_" + file.filename
    )
    with open(image_path, "wb") as file_image:
        file_image.write(contents)
    print("File Uploaded")

    insert_into_csv(
        dataset_csv,
        str(new_id),
        str(label),
    )
    increase_id()

    return {"filename": file.filename, "id": str(new_id), "label": label}
