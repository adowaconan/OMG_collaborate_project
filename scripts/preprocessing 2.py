# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 17:32:32 2018

@author: ning
"""
computer = 'ning'
image_dir = '/home/%s/Downloads/OMG/frames'%computer# directory for saving the frames
import os
import numpy as np
from glob import glob
from tqdm import tqdm
from PIL import Image
from keras.applications.inception_v3 import InceptionV3
pretrained_model = InceptionV3(include_top=False,pooling='avg',)

temp = []
for n in range(7):
    temp_dir = os.path.join(image_dir,str(n))
    images = glob(os.path.join(temp_dir,'*.jpg'))
    for image in tqdm(images,desc='%d'%n):
        try:
            with Image.open(image) as im:
                x, y = im.size
                temp.append([n,x,y])
                
                if (x < 450) and (y < 300):
                    c  = im
                    break
        except:
            print(image)