# This script moves the images correctly classified by the expert into the raw dataset
# and removes their occurences from the files predictions.csv and dataset.csv
import pandas as pd
import os
import glob
import re
import shutil
import numpy as np


dataset_csv = os.path.join("data", "external", "dataset.csv")
predictions_csv = os.path.join("data", "external", "predictions.csv")
dictionary_csv = os.path.join("data", "external", "dictionary.csv")
path_imgs = os.path.join("data", "external", "images")
path_raw_data = os.path.join("data", "raw", "arcDataset")

# Every image name starts with the unique id assigned by the system
imgs_names = [os.path.basename(s) for s in glob.glob(os.path.join(path_imgs, "*"))]
imgs_id = np.array([int(re.split("_", s)[0]) for s in imgs_names])


def clean_data():
    try:
        id_data = []
        id_pred = []
        df_pred = pd.read_csv(predictions_csv)
        df_data = pd.read_csv(dataset_csv)
        df_dict = pd.read_csv(dictionary_csv)

        if not df_pred.empty:
            id_pred = df_pred["id_img"].to_list()

        if not df_data.empty:
            id_data = df_data["id_img"].to_list()

        for id in id_data:

            # Check if the image was priorly classified by the systems
            # and that it exists in the filesystem (by looking in imgs_id)
            if id in id_pred and id in imgs_id:

                # Retrieve the image name corresponding to the its id
                img_name = imgs_names[np.argwhere(imgs_id == id)[0][0]]

                # Retrieve the numeric value of the label corresponding to the image id
                label_id = df_data.loc[df_data["id_img"] == id]["id_class"].values[0]

                # Retrieve the label name from its numerical form
                label = df_dict[str(label_id)][0]

                # Move the image to the raw dataset
                shutil.move(
                    os.path.join(path_imgs, img_name),
                    os.path.join(path_raw_data, label),
                )
                return True
            else:
                return False

    except Exception as e:
        print(e)
