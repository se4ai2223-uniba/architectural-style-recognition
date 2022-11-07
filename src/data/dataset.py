from cmath import e
import os
import shutil
import cv2
import numpy as np
import glob
import random
import tensorflow as tf
import splitfolders

# UNIT TEST
# Behavioral Test
# Invariance
# Directional
# Minimum Functionality

# testare che augment_data produca un numero esatto di samples per ogni classe


class Dataset:
    def __init__(self):
        self.dataset_path = os.path.join("data", "processed", "arcDatasetSelected")
        self.dataset_path_test = os.path.join("data", "processed", "test")
        self.dataset_path_train = os.path.join("data", "processed", "train")
        self.dataset_path_val = os.path.join("data", "processed", "val")

    # Selected classes for the original experiment [0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0]
    def selectClasses(
        self,
        idx=[0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        src_path=os.path.join("data", "raw", "arcDataset"),
        dst_path=os.path.join("data", "processed", "arcDatasetSelected"),
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
            dirs = [
                d
                for d in os.listdir(src_path)
                if os.path.isdir(os.path.join(src_path, d))
            ]
            count = 0

            for el in idx:
                if el == 1:
                    count = count + 1

            if count < 2 or len(idx) != len(dirs):
                return False

            if os.path.exists(dst_path):
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)

            i = 0

            for d in sorted(dirs):
                p = os.path.join(src_path, d)
                if idx[i] == 1:
                    # shutil.copytree creates the folder if it doesn't exists
                    shutil.copytree(p, os.path.join(dst_path, d))
                    print(os.path.join(dst_path, d))
                i = i + 1

        except Exception as e:
            print(e)
            return False

        return True

    def split_dataset(
        self,
        src_path="data/processed/arcDatasetSelected",
        dst_path="data/processed",
        n_instances=30,
    ):

        """
        INPUT:
            -src path
            -dst path

        OUTPUT:
            - folder with a number of instances in the test set for each class
        """
        print(src_path)
        print(dst_path)
        try:

            dir_dict = {}
            for d in os.listdir(src_path):
                if os.path.isdir(os.path.join(src_path, d)):
                    p = os.path.join(src_path, d)
                    # print(p)
                    dir_dict[d] = len(glob.glob(os.path.join(p, "*")))

            print(dir_dict)

            nmin = min(dir_dict.values())

            ## if the number of instances is greater than the 30% of the least represented class
            ## then use the 30% of that class as number to make a uniform distribution of the test set over the classes
            if n_instances >= int(0.3 * nmin):
                n_instances = int(0.3 * nmin)
                if n_instances == 0:
                    n_instances = 1

            ##shutil.copy_tree requires the test folder to exist
            if os.path.exists(os.path.join(dst_path, "test")):
                shutil.rmtree(os.path.join(dst_path, "test"))
                os.mkdir(os.path.join(dst_path, "test"))
            else:
                os.mkdir(os.path.join(dst_path, "test"))

            if os.path.exists(src_path) and os.path.isdir(src_path):
                for d in sorted(os.listdir(src_path)):
                    if os.path.isdir(os.path.join(src_path, d)):

                        ## if the class folder in dst_path does not exist then we create it
                        if not os.path.exists(
                            os.path.join(
                                os.path.join(dst_path, "test"), os.path.basename(d)
                            )
                        ):
                            os.mkdir(
                                os.path.join(
                                    os.path.join(dst_path, "test"), os.path.basename(d)
                                )
                            )

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
                                shutil.move(
                                    f,
                                    os.path.join(
                                        os.path.join(dst_path, "test"),
                                        os.path.basename(p),
                                    ),
                                )
                            n = n + 1

                splitfolders.ratio(
                    src_path,
                    output=dst_path,
                    seed=1337,
                    ratio=(0.7, 0.3),
                    group_prefix=None,
                    move=False,
                )
            else:
                return False
        except Exception as e:
            print(e)
            return False
        return True

    def augment_data(self, path):

        ## Verify if the dataset is already balanced
        counter = []
        try:
            # src = self.dataset_path_train
            # for d in os.listdir(src):
            #     if os.path.isdir(os.path.join(src, d)):
            #         # append in counter the number of non-hidden files in every directory (class)
            #         counter.append(len([f for f in glob.glob(os.path.join(src, d))]))

            # If the dataset is unbalanced then balance it
            if True:

                dir_dict = {}
                # Retrieve the number of files per class
                for d in os.listdir(path):
                    if os.path.isdir(os.path.join(path, d)):
                        print(d)
                        p = os.path.join(path, d)
                        dir_dict[d] = len(
                            [
                                f
                                for f in os.listdir(p)
                                if os.path.isfile(os.path.join(p, f))
                                and not f.startswith(".")
                            ]
                        )
                # Take the number of files in the most represented class
                nmax = max(dir_dict.values())

                for folder in os.listdir(path):

                    if os.path.isdir(os.path.join(path, folder)):
                        # Take the number of files in the current folder
                        length = len(
                            [
                                f
                                for f in os.listdir(os.path.join(path, folder))
                                if os.path.isfile(
                                    os.path.join(os.path.join(path, folder), f)
                                )
                                and not f.startswith(".")
                            ]
                        )

                        ratio = 0.0
                        diff = 0
                        # n_instances = 0

                        # Obtain the ratio between the the most representd class and the current one
                        try:
                            ratio = np.floor((nmax / length))
                            diff = nmax - length
                            # n_instances = np.round(diff / ratio)
                        except:
                            ratio = 0.0
                            # n_instances = 0.0
                        ratio = int(ratio)

                        # Duplicate files until the count difference is zero
                        if ratio == 1:
                            files = [
                                file
                                for file in os.listdir(os.path.join(path, folder))
                                if os.path.isfile(
                                    os.path.join(os.path.join(path, folder), file)
                                )
                                and not file.startswith(".")
                            ]
                            j = diff
                            for file in files:
                                j = j - 1
                                if j >= 0:
                                    src = os.path.join(os.path.join(path, folder), file)
                                    # print("src= ",src)
                                    dst = "copia_" + str(j) + "_" + file
                                    # print("dst= ",dst)
                                    shutil.copy(
                                        src,
                                        os.path.join(os.path.join(path, folder), dst),
                                    )
                        # Duplicate files until the ratio and the count difference are satisfied
                        if ratio > 1:
                            files = [
                                file
                                for file in os.listdir(os.path.join(path, folder))
                                if os.path.isfile(
                                    os.path.join(os.path.join(path, folder), file)
                                )
                                and not file.startswith(".")
                            ]
                            for i in range(ratio):
                                # print("ratio "+str(i))
                                # print("PATH: "+os.path.join(path,folder))
                                for file in files:
                                    new_length = len(
                                        [
                                            f
                                            for f in os.listdir(
                                                os.path.join(path, folder)
                                            )
                                            if os.path.isfile(
                                                os.path.join(
                                                    os.path.join(path, folder), f
                                                )
                                            )
                                            and not f.startswith(".")
                                        ]
                                    )
                                    if (diff - (new_length - length)) > 0:
                                        src = os.path.join(
                                            os.path.join(path, folder), file
                                        )
                                        dst = "copia_" + str(i) + "_" + file
                                        shutil.copy(
                                            src,
                                            os.path.join(
                                                os.path.join(path, folder), dst
                                            ),
                                        )
        except Exception as e:
            print(e)

    def blur(self, path):
        for folder in os.listdir(path):
            for file in os.listdir(os.path.join(path, folder)):
                img = cv2.imread(os.path.join(os.path.join(path, folder), file))
                if img is not None:
                    img = cv2.GaussianBlur(img, (5, 5), 0.85)
                    src = os.path.join(os.path.join(path, folder), file)
                    os.remove(src)
                    cv2.imwrite(src, img)

    def hist_data(self, path):
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

    def getTestSet(self):
        return tf.keras.preprocessing.image_dataset_from_directory(
            self.dataset_path_test,
            labels="inferred",
            label_mode="categorical",
            image_size=(224, 224),
            shuffle=True,
            seed=123,
            batch_size=1,
        )

    def getTrainSet(self):
        return tf.keras.preprocessing.image_dataset_from_directory(
            self.dataset_path_train,
            labels="inferred",
            label_mode="categorical",
            image_size=(224, 224),
            shuffle=True,
            seed=123,
            batch_size=1,
        )

    def getValSet(self):
        return tf.keras.preprocessing.image_dataset_from_directory(
            self.dataset_path_val,
            labels="inferred",
            label_mode="categorical",
            image_size=(224, 224),
            shuffle=True,
            seed=123,
            batch_size=1,
        )
