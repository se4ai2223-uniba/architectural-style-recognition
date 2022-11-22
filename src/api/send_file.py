from fastapi import UploadFile
from pydantic import BaseModel, validator
import requests
import os


#metodo che invia un file all'endpoint adibito
def post_file(endpoint, filepath):
    file = {'file': open(filepath, 'rb')}
    resp = requests.post(url=endpoint, files=file)
    print(resp.json())


post_file('http://127.0.0.1:8000/uploadimage/', 'data/processed/arcDatasetSelected/Achaemenid architecture/21_Tonbeaux-achemenides.JPG')
