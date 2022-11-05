import shutil
import pytest
from src.data.dataset import Dataset
import os
import glob

# Behavioral Test
# Test behavior depending on different arrays

data = Dataset()


@pytest.mark.parametrize(
    "id_sel, valid",
    [
        (
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
            True,
        ),
        (
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            False,
        ),
        ([0, 1, 0, 0, 0, 0, 1, 0, 0, 0], False),
    ],
)
def test_selectClasses(id_sel, valid):
    assert data.selectClasses(idx=id_sel) == valid
    if valid:
        shutil.rmtree(data.dataset_path)


# Integration Test
# test if splitting is successful
def test_splitting():
    assert data.selectClasses()
    assert data.split_dataset()
    assert os.path.exists(data.dataset_path)
    assert os.path.exists(data.dataset_path_test)
    assert os.path.exists(data.dataset_path_train)
    assert os.path.exists(data.dataset_path_val)


# test if data augmentation is producing same number of file in each folder of training
def test_data_augmentation():
    data.augment_data(data.dataset_path_train)
    counter = []
    try:
        src = data.dataset_path_train
        for d in os.listdir(src):
            if os.path.isdir(os.path.join(src, d)):
                # append in counter the number of non-hidden files in every directory (class)
                counter.append(len([f for f in glob.glob(os.path.join(src, d))]))

        assert counter.count(counter[0]) == len(counter)
    except:
        print("Errore! Prova ad eliminare la cartella data.processed.train")
