import os
from src.data.dataset import Dataset
import tensorflow as tf
import tensorflow_hub as hub
from keras.models import model_from_json
from keras.callbacks import EarlyStopping
import yaml


class Params:
    def __init__(self):

        with open("../../params.yaml", "rb") as f:
            conf = yaml.safe_load(f.read())  # load the config file

            self.learning_rate = conf["learning_rate"]
            self.momentum = conf["momentum"]
            self.label_smoothing = conf["label_smoothing"]
            self.dropout_rate = conf["dropout_rate"]
            self.l2 = conf["l2"]
            self.batch_size = conf["batch_size"]
            self.epochs = conf["epochs"]
            self.algorithm = conf["algorithm"]
            self.loss = conf["loss"]
            self.patience = conf["patience"]
            self.early_stopping_metric = conf["early_stopping_metric"]


class Model:
    def __init__(self):

        # create the object for the dataset in order to get the dataset with its methods
        self.data = Dataset()

        # create the object for the paramaters being read from 'params.yaml'
        self.params = Params()

    def buildModel(self, class_names):

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
                tf.keras.layers.Dropout(rate=self.params.dropout_rate),
                tf.keras.layers.Dense(
                    len(class_names),
                    kernel_regularizer=tf.keras.regularizers.l2(self.params.l2),
                    activation="softmax",
                ),
            ]
        )

        model.build((None,) + IMAGE_SIZE + (3,))
        model.summary()

        model.compile(
            optimizer=tf.keras.optimizers.SGD(
                learning_rate=self.params.learning_rate, momentum=self.params.momentum
            ),
            loss=tf.keras.losses.CategoricalCrossentropy(
                from_logits=False, label_smoothing=self.params.label_smoothing
            ),
            metrics=["accuracy"],
        )

        return model

    def trainModel(self):

        if self.params.epochs == None:
            self.params.epochs = 10

        # Creazione del dataset per il training
        ds_train = self.data.getTrainSet()

        class_names = tuple(ds_train.class_names)
        print(class_names)

        # Creazione del dataset per la validation
        ds_validation = self.data.getValSet()

        BATCH_SIZE = self.params.batch_size

        normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)
        normalization2_layer = tf.keras.layers.Normalization(mean=0, variance=1)

        preprocessing_model = tf.keras.Sequential(
            [normalization_layer, normalization2_layer]
        )
        preprocessingVal = tf.keras.Sequential(
            [normalization_layer, normalization2_layer]
        )

        do_data_augmentation = True
        if do_data_augmentation:
            preprocessing_model.add(tf.keras.layers.RandomRotation(40, seed=1337))
            preprocessing_model.add(
                tf.keras.layers.RandomTranslation(0, 0.2, seed=1337)
            )
            preprocessing_model.add(
                tf.keras.layers.RandomTranslation(0.2, 0, seed=1337)
            )
            preprocessing_model.add(tf.keras.layers.RandomZoom(0.2, 0.2, seed=1337))
            preprocessing_model.add(
                tf.keras.layers.RandomFlip(mode="horizontal", seed=1337)
            )

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
        print(valid_size, BATCH_SIZE)
        model = self.buildModel(class_names)

        es = EarlyStopping(
            monitor=self.params.early_stopping_metric,
            mode="min",
            patience=self.params.patience,
            restore_best_weights=True,
            verbose=1,
        )
        hist = model.fit(
            ds_train,
            validation_data=ds_validation,
            epochs=self.params.epochs,
            steps_per_epoch=steps_per_epoch,
            callbacks=[es],
        ).history

        return model, hist

    def saveModel(self, model, path):

        model.save(path)
        model_json = model.to_json()
        with open(os.path.join(path, "model.json"), "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(os.path.join(path, "model.h5"))
        print("Ho salvato il modello!")

    def loadModel(self, path):
        model_loaded = tf.keras.Sequential()
        # load json and create model
        json_file = open(os.path.join(path, "model.json"), "r")
        model_json = json_file.read()
        json_file.close()
        model_loaded = model_from_json(
            model_json, custom_objects={"KerasLayer": hub.KerasLayer}
        )
        # load weights into new model
        model_loaded.load_weights(os.path.join(path, "model.h5"))  # type: ignore
        print("Loaded model from disk")

        return model_loaded
