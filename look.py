# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 17:39:47 2018

@author: ning
"""

import os
import pandas as pd
os.chdir('C:\\Users\\install\\Downloads\\OMGEmotionChallenge-master\\OMGEmotionChallenge-master\\')
transcript_train = pd.read_csv('omg_TrainTranscripts.csv')
Video_train = pd.read_csv('omg_TrainVideos.csv')
import matplotlib.pyplot as plt
import seaborn as sns

# print the columns of the video dataframe
Video_train.columns
# compute the duration of each video
Video_train['duration'] = Video_train['end'] - Video_train['start']
# pairwise plotting
#sns.pairplot(Video_train,hue='EmotionMaxVote')# huge image
sns.pairplot(Video_train[['utterance', 'arousal', 'valence','duration','EmotionMaxVote']],hue='EmotionMaxVote')
# concatenate the two dataframes
df = pd.concat([transcript_train,Video_train],axis=1)
df = df.T.drop_duplicates().T
# get the annotation folder and its subfolders
annotation_folder = 'C:\\Users\\install\\Downloads\\OMGEmotionChallenge-master\\OMGEmotionChallenge-master\\DetailedAnnotation\\train'
os.listdir(annotation_folder)
# print the number of videos and links
print('# of video:',len(pd.unique(df['video'])),', # of link:',len(pd.unique(df['link'])))
# more video than link, so we will have one link corresponds to multiple video ID
# let's see the unique pairs of video and link
video_link = []
for ii,((v,l),d) in enumerate(df.groupby(['video','link'])):# 231 independent data frame
    video_link.append([v,l])

# subsample 100 from the full dataset
samples = df.sample(100)
sns.pairplot(samples[['utterance', 'arousal', 'valence','duration','EmotionMaxVote']],hue='EmotionMaxVote')



# download videos and we will cut the video according to the starts and stops from the dataframe
from pytube import YouTube
#where to save
SAVE_PATH = "D:/OMG" #to_do
links =  pd.unique(df['link'])
for link in links:
    try:
        #object creation using YouTube which was imported in the beginning
        yt = YouTube(link)
    except:
        print("Connection Error") #to handle exception
     
    #filters out all the files with "mp4" extension
    mp4files = yt.filter('mp4')
    #get the video with the extension and resolution passed in the get() function
    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
    try:
        #downloading the video
        d_video.download(SAVE_PATH)
    except:
        print("Some Error!")
print('Task Completed!')
































































































