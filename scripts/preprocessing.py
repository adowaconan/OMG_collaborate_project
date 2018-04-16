#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 13:43:24 2018

@author: ning

This script will:
1. Get clips (segments) of the videos one by one
2. Get frames of each clips/segments and save these frames as individual jpgs
"""
#import cv2
# define paths and directories
computer = 'ning' # adowaconan
video_path = "/home/%s/Downloads/OMG"%computer# videos downloaded from Youtube
saving_dir = "/home/%s/Downloads/OMG/clips"%computer# directory for saving clips
tran_dir = '/home/%s/Downloads/'%computer# directory where your transcript file is
frame_dir = '/home/%s/Downloads/OMG/frames'%computer# directory for saving the frames

# define paths and directories
video_path = "C:/Users/ning/Downloads/OMG"# videos downloaded from Youtube
saving_dir = "C:/Users/ning/Downloads/OMG/clips"# directory for saving clips
tran_dir = 'C:\\Users\\ning\\OneDrive\\python works\\OMG_collaborate_project\\CSVs\\'# directory where your transcript file is
frame_dir = 'C:/Users/ning/Downloads/OMG/frames'# directory for saving the frames

import os
os.chdir(video_path)
if not os.path.exists(saving_dir):
    os.mkdir(saving_dir)
if not os.path.exists(frame_dir):
    os.mkdir(frame_dir)
import pandas as pd
# the concatenated dataframe made before
df = pd.read_csv(tran_dir+'train_concate.csv')
# make more subfolders
for EmotionMaxVote in pd.unique(df['EmotionMaxVote']):# there are 6 unique EmotionMaxVote
    if not os.path.exists(os.path.join(frame_dir,str(EmotionMaxVote))):# for example: /home/adowaconan/Downloads/OMG/frames/1
        os.mkdir(os.path.join(frame_dir,str(EmotionMaxVote)))
from glob import glob
from tqdm import tqdm
import re
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip# function used for clipping videos
from vidpy import Clip # alternative for clipping videos
from vidpy import config
config.MELT_BINARY = '/usr/bin/melt'
videos = glob(os.path.join(video_path,'*mp4.mp4'))# get files that ends with "mp4.mp4" in the video_path

for video in tqdm(videos,desc='video loop'):# for each of the full video
    encode_name = int(re.findall('\d+',video)[0])# get the encoded name, such as 1,2,3,...
    working_df = df[df.encode==encode_name]# get rows that correspond to the same video
    for ii,row in tqdm(working_df.iterrows(),desc='within video loop'): # for each clip of one full video
        t1,t2 = row[['start','end']]# get the start and end time of the clip
        E = row['EmotionMaxVote']# the class
        # round the time to 2 decimals
        t1 = round(t1,2)
        t2 = round(t2,2)
        # define a saving name
        target_name = os.path.join(saving_dir,
                        "%d_%s"%(encode_name,# corresponding to %d - integer placeholder
                                 row['utterance']))# corresponding to %s - string placeholder
        # the main function to clip the video
        # https://superuser.com/questions/1228698/how-do-i-split-a-long-video-into-multiple-shorter-videos-efficiently
#        ffmpeg_extract_subclip(video,t1,t2,targetname=target_name)
        # alternative:
        # https://antiboredom.github.io/vidpy/installation.html#setup
        temp_segment = Clip(video,start=t1,end=t2,)
        temp_segment.save(target_name)
        # small algorithm to get the frames of a clip
        # https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
        vidcap = cv2.VideoCapture(target_name)# load a video to physical memory
        success,image = vidcap.read()# read one frame of a video, if keep running the same line, it will iter through all the frames
        count = 0
        success = True
        sample_interval = 1
        try:
            while success:
            
                print(image.size)
                # define the name of the frame
                for_join = "%d_%s_frame%d.jpg"%(encode_name,# corresponding to the first %d - integer placeholder
                                                row['utterance'].split('.')[0],# corresponding to %s - string placeholder
                                                count)# corresponding to the second %d - integer placeholder
                # join the frame directory
                frame_name = os.path.join(frame_dir+'/%d'%(E),for_join)
                # save the frame
                cv2.imwrite(frame_name,image)
#                for _ in range(sample_interval):
#                    # move to the next frame, if exist any
#                    success,image=vidcap.read()
                print('Read a new frame: ', success)
                count += 1
        except:
            print(target_name)
