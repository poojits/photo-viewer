#!/usr/bin/env python
import cv2
import rgb
import random
import sys
import json
import numpy as np
from numpy import math
import os
from collections import Counter
import shutil

def videoprocessor(data_dir, converted_dir, videoOutput_dir):
    rep_filepath = os.path.join(videoOutput_dir,'rep.json')        
    json_data = open(rep_filepath)
    files = json.load(json_data)
    img_filename = []
    count = 0
    for i in files:
        value = i.values()[0]
        img_filename.append(str(value))
        img_filename[count] = (img_filename[count]).replace('png', 'rgb')
        count += 1
    
    rep_hist = []
    for i in range(0,len(img_filename)):
        filename = os.path.join(data_dir, img_filename[i])
        rgb_image = rgb.imread(filename)
        hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()
        rep_hist.append(hist)
    
    num_video = 10
    video_cluster = []
    for i in range(1,num_video+1):
        filepath = os.path.join(data_dir, 'video%02d.rgb' % i)
        #print filepath
        video = rgb.vdread(filepath)
        image_clusteridx_byfrm = []
        for img in video:
            hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
            hist = cv2.normalize(hist).flatten()
            ref_img_idx = []
            for reference_img in rep_hist:
                ref_img_idx.append(cv2.compareHist(hist,reference_img,cv2.cv.CV_COMP_CHISQR))
            image_clusteridx_byfrm.append(ref_img_idx.index(min(ref_img_idx)))
        frequency = Counter(image_clusteridx_byfrm)
        cluster_index,dumped = frequency.most_common()[0]
        video_cluster.append(int(cluster_index)+1)
        
        
    #moving the video files t the right clusters
    for i in range(1,num_video+1):
        video_name = 'video%02d.ogv' % i
        src = os.path.join(converted_dir,video_name)
        dst = os.path.join(videoOutput_dir,os.path.join('%01d' % video_cluster[i-1],video_name))
        shutil.copy2(src, dst)
        