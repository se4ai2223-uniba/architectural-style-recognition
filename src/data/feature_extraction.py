import os
import cv2
import string
import numpy as np
import great_expectations as ge

def featureExtractor(dataset_raw_path, file_name):
        csv = open(file_name, 'w')
        csv.write('file_name,file_type,label,colors,height,width,img_variance\n')
        for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_raw_path)):
            if dirpath is not path:
                semantic_label = dirpath.split("\\")[-1]
                for f in filenames:                     
                    original_image = cv2.imread(dirpath+'\\'+f)

                    img=cv2.cvtColor(original_image,cv2.COLOR_BGR2RGB)

                    img_name = f.split('.')[0]
                    img_name = img_name.translate(str.maketrans('','',','))
                    
                    img_type = f.split('.')[-1]
                    s = img.shape
                    height = s[0]
                    width = s[1]
                    if((img[:,:,0]==img[:,:,1]).all()==True and (img[:,:,1]==img[:,:,2]).all()==True):
                        colors = 'N'
                    else:
                        colors = 'Y'
                    img_variance = cv2.Laplacian(img, cv2.CV_64F).var()
                    if(img_type!='tmp'):
                        csv.write(img_name+','+img_type+','+semantic_label+','+colors+','+str(height)+','+str(width)+','+str(img_variance)+'\n')
        csv.close()

file_name = 'data\\img_feature\\images_features.csv'
path = 'data\\raw\\arcDataset'
featureExtractor(path, file_name)
