'''This module implement some utilities for the management of the csv datastorage'''
import os
import csv
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image #type:ignore
file_name = os.path.join('data','json','id.json')

def prepare_image(file):
    '''Prepare the image in order that is suitable for the CNN'''
    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

def insert_into_csv(path_json_file, id_image, label):
    '''Insert a computed predition in the relative csv file'''
    header = ['id_img', 'id_class']
    pred = [id_image, label]

    if not os.path.exists(path_json_file):
        with open(path_json_file, 'a', newline='') as predictions_file:
            csv_wr=csv.writer(predictions_file)
            csv_wr.writerow(header)
    with open(path_json_file, 'a', newline='') as predictions_file:
        csv_wr=csv.writer(predictions_file)
        csv_wr.writerow(pred)

def read_id():
    '''Read the id in the id json file'''
    file = open(file_name)
    data = json.load(file)
    i = data['next_id']
    file.close()
    return i

def increase_id():
    '''Increase the id in the id json file'''
    file = open(file_name)
    data = json.load(file)
    file.close()
    data['next_id'] = data['next_id']+1
    file = open(file_name,'w')
    json.dump( data , file)
    file.close()
    