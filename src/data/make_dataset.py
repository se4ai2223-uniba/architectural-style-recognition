# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os 
import shutil
import pandas as pd
import splitfolders
import cv2 
import numpy as np



def augment_data(path):
    dir_dict = {}
    for d in os.listdir(path): 
        if os.path.isdir(os.path.join(path,d)): 
            p = os.path.join(path,d)
            dir_dict[d] = len([f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))])
    nmax = max(dir_dict.values())
    for folder in os.listdir(path): 
        #if(os.path.dirname(folder) != files_names[argmax]):
        length = len([f for f in os.listdir(os.path.join(path,folder))if os.path.isfile(os.path.join(os.path.join(path,folder), f))])
        ratio = 0.0
        diff = 0
        n_instances = 0
        try:
                ratio = np.floor((nmax/length))
                diff = nmax - length
                n_instances = np.round(diff/ratio)
        except:
                ratio = 0.0
                n_instances = 0.0
        ratio = int(ratio)
        if ratio == 1: 
            files = [file for file in os.listdir(os.path.join(path,folder)) 
                 if os.path.isfile(os.path.join(os.path.join(path,folder), file))]
            j = diff
            for file in files:
                j = j - 1
                if j >= 0:
                    src = os.path.join(os.path.join(path,folder),file)
                    #print("src= ",src)
                    dst = 'copia_' + str(j) + '_' + file
                    #print("dst= ",dst)
                    shutil.copy(src,os.path.join(os.path.join(path,folder),dst))
        if ratio > 1: 
            files = [file for file in os.listdir(os.path.join(path,folder)) 
                 if os.path.isfile(os.path.join(os.path.join(path,folder), file))]
            for i in range(ratio):
                #print("ratio "+str(i))
                #print("PATH: "+os.path.join(path,folder))
                for file in files:
                        new_length = len([f for f in os.listdir(os.path.join(path,folder))if os.path.isfile(os.path.join(os.path.join(path,folder), f))])
                        if((diff - (new_length - length))>0):
                            src = os.path.join(os.path.join(path,folder),file)
                            dst = 'copia_' + str(i) + '_' + file
                            shutil.copy(src,os.path.join(os.path.join(path,folder),dst))

def blur(path):
    for folder in os.listdir(path): 
        for file in os.listdir(os.path.join(path,folder)):
                img = cv2.imread(os.path.join(os.path.join(path,folder),file))
                if img is not None:
                  img = cv2.GaussianBlur(img, (5,5), 0.85)
                  src = os.path.join(os.path.join(path,folder),file)
                  os.remove(src)
                  cv2.imwrite(src,img)

def hist_data(path):
    dir_dict = {}
    for d in os.listdir(path): 
        if os.path.isdir(os.path.join(path,d)): 
            p = os.path.join(path,d)
            dir_dict[d] = len([f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))])
    nmax = max(dir_dict.values())
    print(nmax)
    return dir_dict






def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')



    dataset_path = r'data/processed/arcDatasetSplitted/training/'
    dataset_path_test = r'data/processed/arcDatasetSplitted/test/'

    dataset_path_train = r'data/processed/train'
    dataset_path_val = r'data/processed/val'


    splitfolders.ratio(dataset_path, output="data/processed",
    seed=1337, ratio=(.7, .3, .0), group_prefix=None, move=False) # default values

    augment_data(dataset_path_train)
    #augment_data(dataset_path_test)

    ## Noise removal through the use of blurring
    ## and generalization of features inside the images. 
    blur(dataset_path_train)
    blur(dataset_path_val)
    blur(dataset_path_test)




if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
