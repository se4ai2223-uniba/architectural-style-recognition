
from tensorflow.keras.preprocessing import image #type:ignore
import csv
import tensorflow as tf
import numpy as np
import os


#prepara l'immagine in maniera che sia accettabile dalla CNN
def prepare_image(file):
    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

#Inserisce una predizione nel csv
def insert_into_csv(path_json_file, id_image, label):
    header = ['id_img', 'id_class']
    pred = [id_image, label]

    if(not os.path.exists(path_json_file)):
        with open(path_json_file, 'a', newline='') as predictions_file:
            w=csv.writer(predictions_file)
            w.writerow(header)
    with open(path_json_file, 'a', newline='') as predictions_file:
        w=csv.writer(predictions_file)
        w.writerow(pred)

    