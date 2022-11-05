import shutil
import pytest
from src.data.dataset import Dataset
import os
import glob
import utilities as ut
# Behavioral Test
# Test behavior depending on different arrays




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
    data = Dataset()
    assert data.selectClasses(idx=id_sel) == valid
    if valid:
        shutil.rmtree(data.dataset_path)


# Integration Test
# test if splitting is successful
def test_splitting():
    n_instances = 20
    data = Dataset()
    assert data.selectClasses()
    assert data.split_dataset(n_instances=n_instances)
    assert os.path.exists(data.dataset_path)
    assert os.path.exists(data.dataset_path_test)
    assert os.path.exists(data.dataset_path_train)
    assert os.path.exists(data.dataset_path_val)
    counter = ut.count_files(data.dataset_path_test)
    for number in counter:
        assert number == n_instances


# test if data augmentation is producing same number of file in each folder of training
def test_data_augmentation():
    data = Dataset()
    data.selectClasses()
    data.split_dataset()
    data.augment_data(data.dataset_path_train)
    counter = []
    counter = ut.count_files(data.dataset_path_train)
    for number in counter:
        assert number == counter[0]



