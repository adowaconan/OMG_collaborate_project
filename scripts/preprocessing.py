#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 13:43:24 2018

@author: ning
"""
import cv2
# define paths and directories
video_path = "/home/adowaconan/Downloads/OMG"# videos downloaded from Youtube
saving_dir = "/home/adowaconan/Downloads/OMG/clips"# directory for saving clips
tran_dir = '/home/adowaconan/Downloads/'# directory where your transcript file is
frame_dir = '/home/adowaconan/Downloads/OMG/frames'# directory for saving the frames
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
for EmotionMaxVote in pd.unique(df['EmotionMaxVote']):
    if not os.path.exists(os.path.join(frame_dir,str(EmotionMaxVote))):
        os.mkdir(os.path.join(frame_dir,str(EmotionMaxVote)))
from glob import glob
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip# function used for clipping videos
videos = glob(os.path.join(video_path,'*mp4.mp4'))

for video in videos:# for each of the full video
    encode_name = int(re.findall('\d+',video)[0])# get the encoded name, such as 1,2,3,...
    working_df = df[df.encode==encode_name]# get rows that correspond to the same video
    for ii,row in working_df.iterrows(): # for each clip of one full video
        t1,t2 = row[['start','end']]# get the start and end time of the clip
        E = row['EmotionMaxVote']# the class
        t1 = round(t1,2)
        t2 = round(t2,2)
        # define a saving name
        target_name = os.path.join(saving_dir,
                        "%d_%s"%(encode_name,row['utterance']))
        # the main function to clip the video
        # https://superuser.com/questions/1228698/how-do-i-split-a-long-video-into-multiple-shorter-videos-efficiently
        ffmpeg_extract_subclip(video,t1,t2,targetname=target_name)
        # small algorithm to get the frames of a clip
        # https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
        vidcap = cv2.VideoCapture(target_name)
        success,image = vidcap.read()# read one frame of a video, if keep running the same line, it will iter through all the frames
        count = 0
        success = True
        while success:
            # define the name of the frame
            for_join = "%d_%s_frame%d.jpg"%(encode_name,
                                            row['utterance'].split('.')[0],
                                            count)
            # join the frame directory
            frame_name = os.path.join(frame_dir+'/%d'%(E),for_join)
            # save the frame
            cv2.imwrite(frame_name,image)
            # move to the next frame, if exist any
            success,image=vidcap.read()
            print('Read a new frame: ', success)
            count += 1    
        





































































































