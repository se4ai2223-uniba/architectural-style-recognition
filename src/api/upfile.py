from fastapi import UploadFile
import os
from id_manager import read_id, increase_id

from utils import *

# refactoring e modularizzzazoine
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
        os.path.join("..", "..", "data", "external", "dataset.csv"),
        str(new_id),
        str(label),
    )
    increase_id()  
     
    return {"filename": file.filename, "label": label}
