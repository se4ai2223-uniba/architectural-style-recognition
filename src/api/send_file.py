from fastapi import UploadFile
from pydantic import BaseModel, validator
import requests
import os


#metodo che invia un file all'endpoint adibito
def post_file(endpoint, filepath):
    filename, file_extension = os.path.splitext(filepath)
    if(str(file_extension).lower() in ['.jpg', 'bmp', 'gif', 'png',]):
        file = {'file': open(filepath, 'rb')}
        resp = requests.post(url=endpoint, files=file)
        print(resp.json())
    else:
        print("File non riconosciuto")
post_file('http://127.0.0.1:8000/predict/', 'data/processed/arcDatasetSelected/Achaemenid architecture/21_Tonbeaux-achemenides.JPG')