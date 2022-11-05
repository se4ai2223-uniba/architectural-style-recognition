import pytest
import os
import yaml
from src.data.dataset import Dataset
import numpy as np
import os


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

        assert learning_rate > 1e-10
        assert momentum > 1e-10
        assert label_smoothing > 1e-10
        assert dropout_rate > 1e-3
        assert l2 > 1e-15
        assert np.mod(batch_size, 2) == 0  # Batch size must be a multiple of 2
        assert epochs > 0
