# -*- coding: utf-8 -*-
from cmath import e
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
import shutil
import pandas as pd
import splitfolders
import cv2
import numpy as np
import glob
import random


dataset_path = r"data/processed/arcDatasetSelected/"
dataset_path_test = r"data/processed/test/"

dataset_path_train = r"data/processed/train"
dataset_path_val = r"data/processed/val"


def selectClasses(
    idx=[0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    src_path="data/raw/arcDataset",
    dst_path="data/processed/arcDatasetSelected",
):
    """
    INPUT:
        - idx: vector of zeros and ones representing the classes to retain (in lexicoghrapical order)
                i.e. the first position is the first folder in the fyle-system and so on.
        -src path
        -dst path

    OUTPUT:
        - destination folder with the selected classes
    """
    try:
        if os.path.exists(dst_path):
            if os.path.isdir(dst_path):
                shutil.rmtree(dst_path)

        i = 0

        for d in sorted(os.listdir(src_path)):
            if os.path.isdir(os.path.join(src_path, d)):
                p = os.path.join(src_path, d)
                if idx[i] == 1:
                    shutil.copytree(p, os.path.join(dst_path, d))
                    print(os.path.join(dst_path, d))
                i = i + 1

    except Exception as e:
        print(e)


def buildTestSet(
    src_path="data/processed/arcDatasetSelected",
    dst_path="data/processed/test",
    n_instances=30,
):

    """
    INPUT:
        -src path
        -dst path

    OUTPUT:
        - number of instances in the test set for each class
    """

    try:
        dir_dict = {}
        for d in os.listdir(src_path):
            if os.path.isdir(os.path.join(src_path, d)):
                p = os.path.join(src_path, d)
                # print(p)
                dir_dict[d] = len(glob.glob(os.path.join(p, "*")))

        nmin = min(dir_dict.values())

        ## if the number of instances is greater than the 30% of the least represented class
        ## then use the 30% of that class as number to make a uniform distribution of the test set over the classes
        if n_instances >= int(0.3 * nmin):
            n_instances = int(0.3 * nmin)

        ##shutil.copy_tree requires the folder to exist
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
            os.mkdir(dst_path)
        else:
            os.mkdir(dst_path)

        if os.path.exists(src_path) and os.path.isdir(src_path):
            for d in sorted(os.listdir(src_path)):
                if os.path.isdir(os.path.join(src_path, d)):

                    ## if the class folder in dst_path does not exist then we create it
                    if not os.path.exists(os.path.join(dst_path, os.path.basename(d))):
                        os.mkdir(os.path.join(dst_path, os.path.basename(d)))

                    p = os.path.join(src_path, d)

                    # number of files in the folder currently pointed by the for-loop
                    n_files = len(glob.glob(os.path.join(p, "*")))

                    ## vector of zeros and ones for randomly picking test set instances
                    ## one-valued position represent the image to pick
                    ran = np.zeros(n_files + 1)
                    for i in range(1, n_instances):
                        ran[random.randint(1, n_files)] = 1

                    ## since the previuosly "random generated" positions can collide,
                    ## we sequentially fill with ones the remaining n_instances - int(np.sum(ran)) to reach
                    ## the required number of test instances for every class
                    if np.sum(ran) != n_instances:
                        for i in range(1, n_files + 1):
                            if ran[i] == 0 and (n_instances - int(np.sum(ran)) > 0):
                                ran[i] = 1

                    files = [f for f in glob.glob(os.path.join(p, "*"))]
                    n = 1

                    ## now we loop in the folder and, whenever the corresponding vector of position (named 'rand')
                    ## is valued with one, we move the file to the corresponding destination folder
                    for f in files:
                        if ran[n] == 1:
                            shutil.move(f, os.path.join(dst_path, os.path.basename(p)))
                        n = n + 1

    except Exception as e:
        print(e)


def augment_data(path):
    dir_dict = {}
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            p = os.path.join(path, d)
            dir_dict[d] = len(
                [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
            )
    nmax = max(dir_dict.values())
    for folder in os.listdir(path):
        # if(os.path.dirname(folder) != files_names[argmax]):
        length = len(
            [
                f
                for f in os.listdir(os.path.join(path, folder))
                if os.path.isfile(os.path.join(os.path.join(path, folder), f))
            ]
        )
        ratio = 0.0
        diff = 0
        n_instances = 0
        try:
            ratio = np.floor((nmax / length))
            diff = nmax - length
            n_instances = np.round(diff / ratio)
        except:
            ratio = 0.0
            n_instances = 0.0
        ratio = int(ratio)
        if ratio == 1:
            files = [
                file
                for file in os.listdir(os.path.join(path, folder))
                if os.path.isfile(os.path.join(os.path.join(path, folder), file))
            ]
            j = diff
            for file in files:
                j = j - 1
                if j >= 0:
                    src = os.path.join(os.path.join(path, folder), file)
                    # print("src= ",src)
                    dst = "copia_" + str(j) + "_" + file
                    # print("dst= ",dst)
                    shutil.copy(src, os.path.join(os.path.join(path, folder), dst))
        if ratio > 1:
            files = [
                file
                for file in os.listdir(os.path.join(path, folder))
                if os.path.isfile(os.path.join(os.path.join(path, folder), file))
            ]
            for i in range(ratio):
                # print("ratio "+str(i))
                # print("PATH: "+os.path.join(path,folder))
                for file in files:
                    new_length = len(
                        [
                            f
                            for f in os.listdir(os.path.join(path, folder))
                            if os.path.isfile(
                                os.path.join(os.path.join(path, folder), f)
                            )
                        ]
                    )
                    if (diff - (new_length - length)) > 0:
                        src = os.path.join(os.path.join(path, folder), file)
                        dst = "copia_" + str(i) + "_" + file
                        shutil.copy(src, os.path.join(os.path.join(path, folder), dst))


def blur(path):
    for folder in os.listdir(path):
        for file in os.listdir(os.path.join(path, folder)):
            img = cv2.imread(os.path.join(os.path.join(path, folder), file))
            if img is not None:
                img = cv2.GaussianBlur(img, (5, 5), 0.85)
                src = os.path.join(os.path.join(path, folder), file)
                os.remove(src)
                cv2.imwrite(src, img)


def hist_data(path):
    dir_dict = {}
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            p = os.path.join(path, d)
            dir_dict[d] = len(
                [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
            )
    nmax = max(dir_dict.values())
    print(nmax)
    return dir_dict


def main():
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")

    selectClasses()
    buildTestSet()

    splitfolders.ratio(
        dataset_path,
        output="data/processed",
        seed=1337,
        ratio=(0.7, 0.3),
        group_prefix=None,
        move=False,
    )  # default values

    augment_data(dataset_path_train)

    ## Noise removal through the use of blurring
    ## and generalization of features inside the images.
    blur(dataset_path_train)
    blur(dataset_path_val)
    blur(dataset_path_test)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
