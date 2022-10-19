# -*- coding: utf-8 -*-


import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import matplotlib.pylab as plt
import numpy as np

import os
import shutil
import cv2

import pandas as pd
from keras.callbacks import EarlyStopping
import mlflow


def buildModel(class_names, lr, momentum, label_smoothing, dr, l2):

    IMAGE_SIZE = (224, 224)
    mobilenet_v2 = (
        "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
    )
    model = tf.keras.Sequential(
        [
            # Explicitly define the input shape so the model can be properly
            # loaded by the TFLiteConverter
            tf.keras.layers.InputLayer(input_shape=IMAGE_SIZE + (3,)),
            hub.KerasLayer(mobilenet_v2, trainable=True),
            tf.keras.layers.Dropout(rate=dr),
            tf.keras.layers.Dense(
                len(class_names),
                kernel_regularizer=tf.keras.regularizers.l2(l2),
                activation="softmax",
            ),
        ]
    )

    model.build((None,) + IMAGE_SIZE + (3,))
    model.summary()

    model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=lr, momentum=momentum),
        loss=tf.keras.losses.CategoricalCrossentropy(
            from_logits=False, label_smoothing=label_smoothing
        ),
        metrics=["accuracy"],
    )

    return model


def trainModel(epochs):
    mlflow.set_tracking_uri(
        "https://dagshub.com/RobertoLorusso/architectural-style-recognition.mlflow"
    )
    # os.environ["MLFLOW_TRACKING_USERNAME"] = "andreabasile97"
    # os.environ["MLFLOW_TRACKING_PASSWORD"] = "6e3ac8f03201e07f4c0faee9317fc2fd57b6943c"
    mlflow.set_experiment("Training stage")
    mlflow.start_run()

    lr = 0.005
    momentum = 0.9
    label_smoothing = 0.1
    dr = 0.4
    l2 = 0.005
    batch_size = 32
    epochs = 1

    mlflow.log_params(
        {
            "learning-rate": lr,
            "momentum": momentum,
            "lable_smoothing": label_smoothing,
            "dropout-rate": dr,
            "regularized-l2": l2,
            "batch-size": batch_size,
            "epochs": epochs,
            "algorithm": "Stochastic Gradient Descent",
            "loss": "Categorical-Cross-Entropy",
        }
    )

    img_height = 224
    img_width = 224

    if epochs == None:
        epochs = 10

    dataset_path_train = r"data/processed/train/"
    dataset_path_val = r"data/processed/val/"

    # Creazione del dataset per il training
    ds_train = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path_train,
        labels="inferred",
        label_mode="categorical",
        image_size=(img_height, img_width),
        shuffle=True,
        seed=123,
        batch_size=1,
    )

    class_names = tuple(ds_train.class_names)

    print(class_names)

    # Creazione del dataset per la validation
    ds_validation = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path_val,
        labels="inferred",
        label_mode="categorical",
        image_size=(img_height, img_width),
        shuffle=True,
        batch_size=1,
        seed=123,
    )

    BATCH_SIZE = batch_size

    normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)
    normalization2_layer = tf.keras.layers.Normalization(mean=0, variance=1)

    preprocessing_model = tf.keras.Sequential(
        [normalization_layer, normalization2_layer]
    )
    preprocessingVal = tf.keras.Sequential([normalization_layer, normalization2_layer])

    do_data_augmentation = True
    if do_data_augmentation:
        preprocessing_model.add(tf.keras.layers.RandomRotation(40))
        preprocessing_model.add(tf.keras.layers.RandomTranslation(0, 0.2))
        preprocessing_model.add(tf.keras.layers.RandomTranslation(0.2, 0))
        preprocessing_model.add(tf.keras.layers.RandomZoom(0.2, 0.2))
        preprocessing_model.add(tf.keras.layers.RandomFlip(mode="horizontal"))

    train_size = ds_train.cardinality().numpy()
    ds_train = ds_train.unbatch().batch(BATCH_SIZE)
    ds_train = ds_train.repeat()
    ds_train = ds_train.map(
        lambda images, labels: (preprocessing_model(images), labels)
    )

    valid_size = ds_validation.cardinality().numpy()
    ds_validation = ds_validation.unbatch().batch(BATCH_SIZE)
    ds_validation = ds_validation.map(
        lambda images, labels: (preprocessingVal(images), labels)
    )

    # ds_test = ds_test.unbatch().batch(BATCH_SIZE)
    # ds_test = ds_test.map(lambda images, labels:(
    #                         preprocessingVal(images),
    #                         labels))

    steps_per_epoch = train_size // BATCH_SIZE
    validation_steps = valid_size // BATCH_SIZE

    model = buildModel(class_names, lr, momentum, label_smoothing, dr, l2)

    es = EarlyStopping(monitor="val_loss", mode="min", verbose=1)
    hist = model.fit(
        ds_train,
        epochs=epochs,
        steps_per_epoch=steps_per_epoch,
        validation_data=ds_validation,
        validation_steps=validation_steps,
    ).history

    return model, hist


def saveModel(model, path):

    model.save(path)
    model_json = model.to_json()
    with open(os.path.join(path, "model.json"), "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(os.path.join(path, "model.h5"))
    print("Ho salvato il modello!")


model, hist = trainModel(1)
save_path = "models/saved-model"
saveModel(model, save_path)


train_loss = hist["loss"][-1]
val_loss = hist["val_loss"][-1]

train_accuracy = hist["accuracy"][-1]
val_accuracy = hist["val_accuracy"][-1]

mlflow.log_metrics(
    {
        "train_accuracy": train_accuracy,
        "val_accuracy": val_accuracy,
        "train_loss": train_loss,
        "val_loss": val_loss,
    }
)

mlflow.sklearn.log_model(model, "model", registered_model_name="MobileNetV2Archinet")

mlflow.end_run()
