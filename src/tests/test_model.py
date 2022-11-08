import pytest
import os
import yaml
from src.data.dataset import Dataset
import numpy as np
import os
from src.models.model import Model
import shutil
from tensorflow.python.keras.models import model_from_json

orig_path = os.path.join("data", "pytest", "test_data_origin")
src_path = os.path.join("data", "pytest", "test_data")
dst_path = os.path.join("data", "pytest", "apply_test")


def test_params():

    assert os.path.exists("params.yaml")
    with open("params.yaml", "rb") as f:
        conf = yaml.safe_load(f.read())  # load the config file
        learning_rate = conf["learning_rate"]
        momentum = conf["momentum"]
        label_smoothing = conf["label_smoothing"]
        dropout_rate = conf["dropout_rate"]
        l2 = conf["l2"]
        batch_size = conf["batch_size"]
        epochs = conf["epochs"]

        assert isinstance(learning_rate, float)
        assert isinstance(momentum, float)
        assert isinstance(label_smoothing, float)
        assert isinstance(dropout_rate, float)
        assert isinstance(l2, float)
        assert isinstance(epochs, int)

        assert learning_rate > 1e-10
        assert momentum > 1e-10
        assert label_smoothing > 1e-10
        assert dropout_rate > 1e-3
        assert l2 > 1e-15
        assert np.mod(batch_size, 2) == 0  # Batch size must be a multiple of 2
        assert epochs > 0


def test_buildModel():
    model_ = Model()
    class_names = ["dummy1", "dummy2", "dummy3"]
    model = model_.buildModel(class_names)

    assert model.layers[0].input.shape == (None, 224, 224, 3)
    assert model.layers[-1].output.shape == (None, len(class_names))


def test_trainModel():
    model_ = Model()
    data = Dataset()

    if os.path.exists(src_path):
        shutil.rmtree(src_path)
    shutil.copytree(orig_path, src_path)

    # creazione del train dummy
    data.split_dataset(src_path=src_path)
    data.augment_data(data.dataset_path_train)

    model_.params.batch_size = 5
    model_.params.epochs = 3
    model_.params.early_stopping_metric = "loss"
    model_.params.patience = 1

    # fitting del modello dummy sul train dummy
    model, hist = model_.trainModel()

    print(hist["loss"][0], hist["loss"][-2])

    # assert that loss decrease
    assert hist["loss"][0] > hist["loss"][-2]
    shutil.rmtree(src_path)
