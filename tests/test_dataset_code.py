import shutil
import pytest
from src.data.dataset import Dataset 
import os

# Behavioral Test
# Test behavior depending on different arrays

data = Dataset()

@pytest.mark.parametrize(
    "id_sel, valid",
    [
        ([0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0], True),
        ([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], False),
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
def test_data_augumentation():
    data.augment_data(data.dataset_path_train)
    number_of_files = 0
    array_counter = []
    try:
        for d in os.listdir(data.dataset_path_train):
            if(d != '.DS_Store'):
                for root_dir, cur_dir, files in os.walk(os.path.join(data.dataset_path_train, d)):
                    number_of_files += len(files)
                array_counter.append(number_of_files)
                number_of_files = 0
        for i in range (len(array_counter)-1):
            assert array_counter[i] == array_counter[i+1]
    except: 
        print("Errore! Prova ad eliminare la cartella data.processed.train")
