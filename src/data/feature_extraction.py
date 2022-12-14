"""
This module implements the feature extraction of the images in the dataset.
These feature are then stored in a csv file and processed by Great Expectations.
"""
import os
import cv2


def feature_extractor(dataset_raw_path, file_name):
    """Function that implements the feature extraction"""
    csv = open(file_name, "w")
    csv.write("file_name,file_type,label,colors,height,width,img_variance\n")
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_raw_path)):
        if dirpath is not path:
            # Modify dirpath.split("\\") with machine os.path....
            semantic_label = os.path.basename(dirpath)
            for f in filenames:
                # hidden files will be ignored
                if not f.startswith("."):
                    original_image = cv2.imread(os.path.join(dirpath, f))

                    img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

                    img_name = f.split(".")[0]

                    img_name = img_name.translate(str.maketrans("", "", ","))

                    img_type = f.split(".")[-1]
                    if img_type != "tmp":

                        img_shape = img.shape
                        height = img_shape[0]
                        width = img_shape[1]
                        if (img[:, :, 0] == img[:, :, 1]).all() == True and (
                            img[:, :, 1] == img[:, :, 2]
                        ).all() == True:
                            colors = "N"
                        else:
                            colors = "Y"
                        img_variance = cv2.Laplacian(img, cv2.CV_64F).var()

                        csv.write(
                            img_name
                            + ","
                            + img_type
                            + ","
                            + semantic_label
                            + ","
                            + colors
                            + ","
                            + str(height)
                            + ","
                            + str(width)
                            + ","
                            + str(img_variance)
                            + "\n"
                        )
    csv.close()


FILE_NAME = os.path.join("data", "img_feature", "images_features.csv")
path = os.path.join("data", "raw", "arcDataset")
feature_extractor(path, FILE_NAME)
