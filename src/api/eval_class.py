import pandas as pd
import os
from utils import *


dataset_csv = os.path.join("..", "..", 'data','external','dataset.csv')
classification_csv = os.path.join("..", "..", 'data','external','predictions.csv')

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