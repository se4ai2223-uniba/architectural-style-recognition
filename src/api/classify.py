from fastapi import UploadFile
import numpy as np
import os
from id_manager import read_id, increase_id

from utils import *
import pandas as pd

# riceve un'immagine e fornisce la predizione. l'immagine e la predizione vengono salvate.

# refactoring e modularizzzazoine
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
        os.path.join("..", "..", "data", "external", "predictions.csv"),
        str(nuovo_id),
        str(label),
    )
    increase_id()
    if os.path.exists(os.path.join("..", "..", "data", "external", "dictionary.csv")):
        df = pd.read_csv(os.path.join("..", "..", "data", "external", "dictionary.csv"))
        label = df[str(label)][0]
        del df

    return {"filename": file.filename, "id": str(nuovo_id), "label": label}
