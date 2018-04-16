# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 17:32:32 2018

@author: ning
"""
computer = 'ning'
image_dir = '/home/%s/Downloads/OMG/frames'%computer# directory for saving the frames
image_dir = 'C:\\Users\\ning\\Downloads\\OMG\\frames'
image_resize_dir = 'C:\\Users\\ning\\Downloads\\OMG\\resize'
import os
import numpy as np
from glob import glob
from tqdm import tqdm
from PIL import Image
from keras.applications.inception_v3 import InceptionV3

if not os.path.exists(image_resize_dir):
    os.mkdir(image_resize_dir)
temp = []
for n in range(7):
    if not os.path.exists(image_resize_dir+'\\'+str(n)):
        os.mkdir(image_resize_dir+'\\'+str(n))
    temp_dir = os.path.join(image_dir,str(n))
    images = glob(os.path.join(temp_dir,'*.jpg'))
    for image in tqdm(images,desc='%d'%n):
        
        with Image.open(image) as im:
            x, y = im.width,im.height
            temp.append([n,x,y])
            file_name = image.split('\\')[-1]
            new_name = image_resize_dir+'\\'+str(n)+'\\'+file_name
            im.resize((360,640))
            im.save(new_name)
                

import pandas as pd
df = pd.DataFrame(temp,columns=['emotion','w','h'])
pretrained_model = InceptionV3(include_top=False,pooling='avg',input_shape=(360,640,3))












































































