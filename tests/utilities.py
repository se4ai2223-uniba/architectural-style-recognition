from src.data.dataset import Dataset
import os

# count how many files there are for each folder inside src
def count_files(src):
    counter = []
    count = 0
    for d in os.listdir(src):
        for root_dir, cur_dir, files in os.walk(os.path.join(src, d)):
            count += len(files)
        counter.append(count)
        count = 0
    return counter
