# -*- coding: utf-8 -*-
import os
import logging
from pathlib import Path
from dotenv import find_dotenv
import numpy as np
from dotenv import dotenv_values
from src.data.dataset import Dataset


def main():
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("Making final data set from raw data")

    data = Dataset()
    ## Here we select only two classes for test purposes, making the training time very short
    ## if you want to retain the 10 classes selected in the original experiment, just call selectedClasses without any param
    idx = np.zeros(25)
    idx[0] = 1
    idx[1] = 1
    data.selectClasses(idx=idx)
    data.make_dict()
    data.split_dataset()

    # default values

    data.augment_data(data.dataset_path_train)

    ## Noise removal through the use of blurring
    ## and generalization of features inside the images.
    data.blur(data.dataset_path_train)
    data.blur(data.dataset_path_val)
    data.blur(data.dataset_path_test)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())
    conf = dotenv_values(find_dotenv())
    os.environ["MLFLOW_TRACKING_USERNAME"] = conf["MLFLOW_TRACKING_USERNAME"]  # type: ignore
    os.environ["MLFLOW_TRACKING_PASSWORD"] = conf["MLFLOW_TRACKING_PASSWORD"]  # type: ignore

    main()
