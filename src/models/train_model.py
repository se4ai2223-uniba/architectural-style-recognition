# -*- coding: utf-8 -*-


from json import load
import tensorflow as tf
from tensorflow import keras
from tensorflow.math import confusion_matrix
from tensorflow.keras import layers
import tensorflow_hub as hub
import matplotlib.pylab as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os 
import shutil
import cv2
from tensorflow.keras.models import model_from_json
import pandas as pd
from keras.callbacks import EarlyStopping




def buildModel(class_names):
    

    IMAGE_SIZE = (224, 224)
    mobilenet_v2 = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
    model = tf.keras.Sequential([
        # Explicitly define the input shape so the model can be properly
        # loaded by the TFLiteConverter
        tf.keras.layers.InputLayer(input_shape=IMAGE_SIZE + (3,)),
        hub.KerasLayer(mobilenet_v2, trainable=True),
        tf.keras.layers.Dropout(rate=0.4),
        tf.keras.layers.Dense(len(class_names),
                             kernel_regularizer=tf.keras.regularizers.l2(0.005),
                             activation="softmax"
                             )
    ])

    model.build((None,)+IMAGE_SIZE+(3,))
    model.summary()

    model.compile(
      optimizer=tf.keras.optimizers.SGD(learning_rate=0.005, momentum=0.9), 
      loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False, label_smoothing=0.1),
      metrics=['accuracy'])

      
    return model






def trainModel(epochs):

    
    img_height = 224
    img_width = 224

    if epochs == None :
        epochs = 10

    
    dataset_path_test = r'data/processed/arcDatasetSplitted/test/'

    dataset_path_train = r'data/processed/train/'
    dataset_path_val = r'data/processed/val/'


#Creazione del dataset per il training
    ds_train = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path_train,
        labels='inferred',
        label_mode = 'categorical',
        image_size = (img_height, img_width),
        shuffle=True,
        seed=123,
        batch_size=1)

    class_names = tuple(ds_train.class_names)
    

    print(class_names)

    #Creazione del dataset per la validation
    ds_validation = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path_val,
        labels='inferred',
        label_mode = 'categorical',
        image_size = (img_height, img_width),
        shuffle=True,
        batch_size=1,
        seed=123)

    ds_test = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path_test,
        labels='inferred',
        label_mode = 'categorical',
        image_size = (img_height, img_width),
        shuffle=True,
        seed=123,
        batch_size=1)


    BATCH_SIZE = 32



    normalization_layer = tf.keras.layers.Rescaling(1. / 255)
    normalization2_layer = tf.keras.layers.Normalization(mean=0, variance=1)

    preprocessing_model = tf.keras.Sequential([normalization_layer, normalization2_layer])
    preprocessingVal = tf.keras.Sequential([normalization_layer, normalization2_layer])

    do_data_augmentation = True
    if do_data_augmentation:
      preprocessing_model.add(
          tf.keras.layers.RandomRotation(40))
      preprocessing_model.add(
          tf.keras.layers.RandomTranslation(0, 0.2))
      preprocessing_model.add(
          tf.keras.layers.RandomTranslation(0.2, 0))
      preprocessing_model.add(
          tf.keras.layers.RandomZoom(0.2, 0.2))
      preprocessing_model.add(
          tf.keras.layers.RandomFlip(mode="horizontal"))


    train_size = ds_train.cardinality().numpy()
    ds_train = ds_train.unbatch().batch(BATCH_SIZE)
    ds_train = ds_train.repeat()
    ds_train = ds_train.map(lambda images, labels:
                            (preprocessing_model(images), labels))

    valid_size = ds_validation.cardinality().numpy()
    ds_validation = ds_validation.unbatch().batch(BATCH_SIZE)
    ds_validation = ds_validation.map(lambda images, labels:
                        (
                            preprocessingVal(images),
                            labels))

    ds_test = ds_test.unbatch().batch(BATCH_SIZE)
    ds_test = ds_test.map(lambda images, labels:(
                            preprocessingVal(images),
                            labels))

    

    
 

    steps_per_epoch = train_size // BATCH_SIZE 
    validation_steps = valid_size // BATCH_SIZE 

    



    model = buildModel(class_names)

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
    hist = model.fit(
        ds_train,
        epochs=epochs,
        steps_per_epoch=steps_per_epoch ,
        validation_data=ds_validation,
        validation_steps=validation_steps
        ).history

    
    return model,hist




def loadModel(path): 

    model_loaded = tf.keras.Sequential()
    # load json and create model
    json_file = open(os.path.join(path,'model.json'), 'r')
    model_json = json_file.read()
    json_file.close()
    model_loaded = model_from_json(model_json, custom_objects={'KerasLayer': hub.KerasLayer})
    # load weights into new model
    model_loaded.load_weights(os.path.join(path,"model.h5"))
    print("Loaded model from disk")


def saveModel(model,path):

    model.save(path)
    model_json = model.to_json()
    with open(os.path.join(path,'model.json'), "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(os.path.join(path,'model.h5'))
    print("Ho salvato il modello!")





model,hist = trainModel(1)
save_path = "models/saved-model"
saveModel(model,save_path)
