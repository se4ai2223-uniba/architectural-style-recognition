import shutil
import pytest
from src.data.dataset import Dataset
import os
import utilities as ut # type: ignore

# Behavioral Test
# Test behavior depending on different arrays

orig_path = os.path.join("data", "pytest", "test_data_origin")
src_path = os.path.join("data", "pytest", "test_data")
dst_path = os.path.join("data", "pytest", "apply_test")
data = Dataset()


@pytest.fixture(autouse=True)
def prepareTestData():

    if os.path.exists(src_path):
        shutil.rmtree(src_path)

    shutil.copytree(orig_path, src_path)
    yield src_path
    shutil.rmtree(src_path)
    if os.path.exists(dst_path):
        ut.remove_content(dst_path)


@pytest.mark.parametrize(
    "id_sel, valid",
    [
        (
            [0, 0, 0, 1, 1],
            True,
        ),
        (
            [0, 1, 0, 0, 0],
            False,
        ),
        ([0, 1, 0, 0, 0, 0, 1, 0, 0, 0], False),
        ([0, 1, 0], False),
    ],
)
def test_selectClasses(id_sel, valid):
    # shutil.copytree(orig_path, src_path)
    assert (
        data.selectClasses(
            src_path=src_path,
            dst_path=dst_path,
            idx=id_sel,
        )
        == valid
    )


# Integration Test
# test if splitting is successful
def test_splitting():

    n_instances = 1
    assert data.split_dataset(
        src_path=src_path, dst_path=dst_path, n_instances=n_instances
    )
    assert os.path.exists(src_path)
    assert os.path.exists(os.path.join(dst_path, "test"))
    assert os.path.exists(os.path.join(dst_path, "train"))
    assert os.path.exists(os.path.join(dst_path, "val"))
    counter_test = ut.count_files(os.path.join(dst_path, "test"))
    for number in counter_test:
        assert number == n_instances
    counter_train = ut.count_files(os.path.join(dst_path, "train"))
    counter_val = ut.count_files(os.path.join(dst_path, "val"))
    assert len(counter_test) == len(counter_train) == len(counter_val)


# test if data augmentation is producing same number of file in each folder of training
def test_data_augmentation():

    data.augment_data(src_path)
    counter = []
    counter = ut.count_files(src_path)
    print(counter)
    for number in counter:
        assert number == counter[0]
