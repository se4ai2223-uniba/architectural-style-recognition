from typing import Tuple, Generator, Callable, Optional
import os
import numpy as np
import torch
import torch.nn as nn
import cv2
from torch.utils.data import TensorDataset, DataLoader
from torchvision import datasets, transforms
from alibi_detect.cd import MMDDriftOnline
from statistics import mean 

torch.manual_seed(0)
np.random.seed(0)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class DriftDetector:
  def __init__(self):
    ref_path = os.path.join('data','external','ref_data')
    encoder_path = os.path.join('models','autoencoder_drift_detector','encoder.pkl')
    self.n_average = 5
    self.arr_ddfc = [0 for x in range(self.n_average)] # detection delay following change
    self.avg_index = 0
    self.avg = 0

    ERT = 50  # expected run-time in absence of change
    W = 10  # size of test window

    ds = datasets.ImageFolder(ref_path, transforms.Compose([
        transforms.ToTensor()
    ]))
    N = len(ds)
    di =iter(torch.utils.data.DataLoader(ds, batch_size=1, shuffle=True))
    ref = np.stack([next(di)[0][0].numpy() for _ in range(N)], axis=0)

    encoder = torch.load(encoder_path)

    def encoder_fn(x: np.ndarray) -> np.ndarray:
      x = torch.as_tensor(x).to(device)
      with torch.no_grad():
          x_proj = encoder(x)
      return x_proj.cpu().numpy()

    self.dd = MMDDriftOnline(ref, ERT, W, backend='pytorch', preprocess_fn=encoder_fn)
    self.drift = False
    self.t = 0  

  def is_drift(self, file):  
    if(self.drift):
      self.dd.reset() 
      self.t = 0
    # Read the image
    image = cv2.imread(file)      
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    dim = (96, 96)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    transform=transforms.Compose([
        transforms.ToTensor()])
      
    # Convert the image to Torch tensor
    tensor = transform(image).numpy()
      
    # print the converted image tensor
    self.drift = self.dd.predict(tensor)['data']['is_drift']
    self.t = self.t + 1
    if(self.drift):
        self.arr_ddfc[self.avg_index]=self.t
        self.avg = mean(self.arr_ddfc) 
        self.avg_index+=1
        self.avg_index = self.avg_index%self.n_average
    return (self.drift, self.t, self.avg)