import os
import shutil
from src.data.dataset import Dataset
import glob
import numpy as np

# count how many files there are for each folder inside src
def count_files(src):
    counter = []

    dirs = [d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d))]

    for d in dirs:
        counter.append(len(glob.glob(os.path.join(os.path.join(src, d), "*"))))

    return counter


def remove_content(path):

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

