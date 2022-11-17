from typing import Union
from fastapi import FastAPI, File, UploadFile
import shutil
import os
import aiofiles
from os.path import join as join

app = FastAPI()


# Asyncronous saving of file
@app.post("/uploadfiles/")
async def create_upload_file(file: UploadFile, q: Union[str, None] = None):

    try:
        async with aiofiles.open(
            join(join("../../data", "external"), file.filename),
            "wb",
        ) as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
    except:
        print("Ex")
    finally:
        file.file.close()
        return {"filename": file.filename}


# Syncronous saving of file
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, user: Union[str, None] = None):

    try:
        data_path = join(join(join("..", ".."), "data"), "external")
        with open(join(data_path, file.filename), "wb") as buffer:
            shutil.copyfileobj(file, buffer)
    except:
        print("Ex")
    finally:
        file.file.close()
        return {"filename": file.filename, "User": user}
