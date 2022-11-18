from fastapi import FastAPI
import json
import pandas as pd
import os

app = FastAPI()
dataset_csv = os.path.join('..','..','data','external','dataset.csv')
classification_csv = os.path.join('..','..','data','external','predictions.csv')

def evaluate_classification(id, classification):
    idsd = []
    dfc = pd.read_csv(classification_csv)
    
    dfd = pd.read_csv(dataset_csv)
    if not dfc.empty:
        idsc = dfc["id_img"].to_list()
    if not dfd.empty:
        idsd = dfd["id_img"].to_list()
    if (id in idsc and id not in idsd):
        dfd_ins = pd.DataFrame([[id, classification]], columns=['id_img', 'id_class'])        
        dfd=pd.concat([dfd, dfd_ins])  

        print(dfd)
        dfd.to_csv(dataset_csv, index=False)  
        return 'ok'
    else:
        return 'ko'

@app.post("/eval_class/")
async def eval_class( id_img: int, new_class: str):
    res = evaluate_classification(id_img, new_class)
    return {"result": res}