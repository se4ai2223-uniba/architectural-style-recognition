from http.client import HTTPException
from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from tensorflow.keras.applications import imagenet_utils #type:ignore
from tensorflow.keras.preprocessing import image #type:ignore
from tensorflow.keras.models import model_from_json #type:ignore
import os

app = FastAPI()

from fastapi import FastAPI

app = FastAPI()

# Esempio di path marameters che deve essere per forza un intero
@app.post("/uploadimage/")
async def create_upload_image(file: UploadFile):
    contents = await file.read()
    generated_id = generate_id(os.path.join('..','..','data','external', 'ids.txt'))
    image_path = os.path.join('..','..','data','external', 'images', str(generated_id) + "_" + file.filename)
    with open(image_path, "wb") as f:
        f.write(contents)
    with open(os.path.join('..','..','data','external', 'ids.txt'), 'a') as id_file:
        id_file.write(str(generated_id)+"\n")
        id_file.close() 
    print("File Uploaded")
    path_saved_model = os.path.join('..','..','models','saved-model-optimal/')
    model = load_model(path_saved_model)
    preprocessed_image = prepare_image(image_path)
    predictions = model.predict(preprocessed_image)
    label = np.argmax(predictions)
    return {"filename": file.filename, "label": str(label)}

def load_model(path):
    model_loaded = tf.keras.Sequential()
    # load json and create model
    json_file = open(path+'model.json', 'r')
    model_json = json_file.read()
    json_file.close()
    model_loaded = model_from_json(model_json, custom_objects={'KerasLayer': hub.KerasLayer})
    # load weights into new model
    model_loaded.load_weights(path+"model.h5")
    return model_loaded

def prepare_image(file):
    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

def generate_id(ids_path_file):
    id_founded = []
    i=0
    try:
        # Inserisci tutti gli id relative alle immagini presenti in /images
        with open(ids_path_file, 'w') as id_file:
            for image in os.listdir(os.path.join('..','..','data','external', 'images')):
                id = image.split('_')[0]
                id_founded.append(id)
                id_file.write(str(id)+"\n")
            print(id_founded)
            id_file.close() 
        while(str(i) in id_founded):
            i=i+1
        return i
    except:
        return 0

generate_id(os.path.join('..','..','data','external', 'ids.txt'))

    