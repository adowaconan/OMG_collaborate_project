# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 17:32:32 2018

@author: ning

run this in the terminal first:
    pip install --upgrade keras
    
making sure you use keras 2.1.5
"""
# define working and saving directories
computer = 'ning'
#image_dir = '/home/%s/Downloads/OMG/frames'%computer# directory for saving the frames
image_dir = 'C:\\Users\\ning\\Downloads\\OMG\\frames'
image_resize_dir = 'C:\\Users\\ning\\Downloads\\OMG\\resize'
image_resize_png_dir  = 'C:\\Users\\ning\\Downloads\\OMG\\resize_png'
#image_resize_dir = '/home/%s/Downloads/OMG/resize'%computer
import os
import numpy as np
from glob import glob
from tqdm import tqdm
from PIL import Image
from keras.applications.vgg19 import VGG19,preprocess_input

if not os.path.exists(image_resize_dir):# create a resize directory
    os.mkdir(image_resize_dir)
if not os.path.exists(image_resize_png_dir):# create a directory for converting jpg images to png images
    os.mkdir(image_resize_png_dir)
temp = []
for n in range(7):# if you are not running this in windows os, change "\\" to "/"
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
            im = im.resize((512,512))
            im.save(new_name)
                

import pandas as pd
df = pd.DataFrame(temp,columns=['emotion','w','h'])
pretrained_model = VGG19(include_top=False,# don't need the top layer
                         classes=7,# 7 classes
                         pooling='avg',# global averages for the last layer
                         input_shape=(512,512,3),)# input dimensionality
# freeze the layers
for layer in pretrained_model.layers:
    layer.trainable = False

from keras.preprocessing.image import ImageDataGenerator
Generator = ImageDataGenerator(rotation_range=10,# for robustness
                               horizontal_flip=True,# for robustness
                               vertical_flip=True,# for robutsness
                               rescale=1./255,# rescale preprocessing
                               validation_split=0.1,)# split 10% to be validation data
#                               preprocessing_function=preprocess_input)
# get the training images
train_generator = Generator.flow_from_directory(image_resize_dir,
                                                target_size=(512,512),
                                                batch_size=32,
#                                                save_to_dir=image_resize_png_dir,
                                                subset='training')
# get the validation images
validation_generator=Generator.flow_from_directory(image_resize_dir,
                                                target_size=(512,512),
                                                batch_size=1,shuffle=False,
                                                subset='validation')


from keras.layers import Dense
from keras import Model
from keras.optimizers import Adam
output = pretrained_model.output # get the output of the layer
#output = Dense(1024,activation='relu',)(output)# stack more layers
#output = Dense(64,activation='relu')(output)# stack more layers
output = Dense(7,activation='softmax')(output)# the very last layers must be a softmax classifier
model = Model(pretrained_model.input,output,name='model')# put everything together
model.compile(optimizer=Adam(),loss='mse',metrics=['mse'])# compile the model a optimizer, a loss function, and a metrics for measuring the loss
# fit the model
#model.fit_generator(train_generator,)
# predict the labels
pred = model.predict_generator(validation_generator,steps=None)









































































