from fastapi import FastAPI
import json
import pandas as pd
import os

app = FastAPI()
dataset_json = os.path.join('data','json','dataset.json')
classification_json = os.path.join('data','json','classification.json')

def evaluate_classification(id, classification):
    idsd = []
    dfc = pd.read_json(classification_json)
    
    dfd = pd.read_json(dataset_json)
    if not dfc.empty:
        idsc = dfc["id_img"].to_list()
    if not dfd.empty:
        idsd = dfd["id_img"].to_list()
    if (id in idsc and id not in idsd):
        dfd_ins = pd.DataFrame([[id, classification]], columns=['id_img', 'classification'])        
        dfd=pd.concat([dfd, dfd_ins])  
        parsed = json.loads(dfd.to_json(orient='records'))
        f = open(dataset_json,'w')
        json.dump(parsed , f, indent=4)
        f.close()
        return 'ok'
    else:
        return 'ko'

@app.post("/eval_class/")
async def eval_class( id_img: int, new_class: str):
    res = evaluate_classification(id_img, new_class)
    return {"result": res}

evaluate_classification(2, 'bobo')
