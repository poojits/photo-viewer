#!/usr/bin/env python
import cv2
import rgb
import numpy as np
import os
import shutil
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
import getopt
import sys
from timeit import itertools
import json
import random
import videoClassifier
import time

num_files = 300


def usage():
    msg = '''Usage: python main.py -d <data directory> -c <converted data directory> -o <output directory>'''
    print msg

def count(labels, k):
    c = [0] * k
    for i,l in enumerate(labels):
        c[l] += 1
    return c
        

def mymkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_image_features(data_dir):
    #-------------------------constructing histograms-------------------------------
    
    data = []
    for n in range(1, num_files+1):
        filename = os.path.join(data_dir, 'image%03d.rgb' % n)
        rgb_image = rgb.imread(filename)
        hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()
        data.append(hist)
    return data

    #---------------------------------------------------------------------------------


#-----------------------------FACE/NON-FACE----------------------------------
def partition_faces(data_dir, converted_dir, output_dir):
    #path for haarcascade_frontalface_default.xml
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    idx = []
    face_path = os.path.join(output_dir, "face")
    nonface_path = os.path.join(output_dir, "nonface")
    if os.path.isdir(face_path):
        shutil.rmtree(face_path)
    if os.path.isdir(nonface_path):
        shutil.rmtree(nonface_path)
    mymkdir(face_path)
    mymkdir(nonface_path)
    for n in range(1, num_files+1):
        filename = os.path.join(data_dir, 'image%03d.rgb' % n)
        img = rgb.imread(filename)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, 1.05, 4, 0, (40,40))
        png_path = os.path.join(converted_dir, 'image%03d.png' % n)
        if len(faces):
            idx.append(1)
            shutil.copy2(png_path, face_path)
            #for (x,y,w,h) in faces:
            #    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
            #cv2.imshow('face', img)
            #cv2.waitKey(0)
        if not len(faces):
            idx.append(2)
            shutil.copy2(png_path, nonface_path)
    return idx

    #--------------------------------------------------------------


#------------------CLUSTERING OF FACES--------------------------
def cluster_faces(data, idx, output_dir):
    #faces
    modified_data = []
    fileindex = []
    for n in range(0, num_files):
        if idx[n] == 1:
            modified_data.append(data[n])
            fileindex.append(n)

    criteria = (cv2.TERM_CRITERIA_EPS, 100, 1.0)
    K = 8
    ret, label, center = cv2.kmeans(np.array(modified_data), K, criteria, 10, cv2.KMEANS_PP_CENTERS)
    face_path = os.path.join(output_dir, 'face')
    
    #Representatives 
    min_distance = [9999999] * K
    corres_idx = [0] * K 
    for x in range(1, K+1):
        for i, l in enumerate(label):
            if l == x-1:
                d = np.linalg.norm(center[l]-modified_data[i])
                if d < min_distance[l]:
                    min_distance[l] = d
                    corres_idx[l] = i 
                    
    representative = []
    for i, idx in enumerate(corres_idx):
        obj = {}
        obj[i+1] = 'image%03d.png' % (fileindex[idx] + 1)
        representative.append(obj)
    f = open(os.path.join(face_path, 'rep.json'), 'w')
    f.write(json.dumps(representative))
    f.close()
    #end of reps
    
    for l in range(1, K+1):
        mymkdir(os.path.join(face_path, '%d' % l))
    for i, l in enumerate(label):
        png_path = os.path.join(face_path, 'image%03d.png' % (fileindex[i]+1))
        shutil.move(png_path, os.path.join(face_path, '%d' % (int(l)+1)))
    #end_faces
    #-------------------------------------------------------------------------------------------------


#-------------------------CLUSTERING NON FACES----------------------------------------------------
def cluster_nonfaces(data, idx, output_dir):
    #non faces
    modified_data = []
    fileindex = []
    for n in range(0, num_files):
        if idx[n] ==2:
            modified_data.append(data[n])
            fileindex.append(n)

    criteria = (cv2.TERM_CRITERIA_EPS, 100, 1.0)
    K = 8
    ret, label, center = cv2.kmeans(np.array(modified_data), K, criteria, 100, cv2.KMEANS_PP_CENTERS)
    nonface_path = os.path.join(output_dir, 'nonface')
    
    #Representatives 
    min_distance = [9999999] * K
    corres_idx = [0] * K 
    for x in range(1, K+1):
        for i, l in enumerate(label):
            if l == x-1:
                d = np.linalg.norm(center[l]-modified_data[i])
                if d < min_distance[l]:
                    min_distance[l] = d
                    corres_idx[l] = i 

    representative = []
    for i, idx in enumerate(corres_idx):
        obj = {}
        obj[i+1] = 'image%03d.png' % (fileindex[idx] + 1)
        representative.append(obj)
    #print json.dumps(representative)
    f = open(os.path.join(nonface_path, 'rep.json'), 'w')
    f.write(json.dumps(representative))
    f.close()
    #end of reps
    
    for l in range(1, K+1):
        mymkdir(os.path.join(nonface_path, '%d' % l))
    for i, l in enumerate(label):
        png_path = os.path.join(nonface_path, 'image%03d.png' % (fileindex[i]+1))
        shutil.move(png_path, os.path.join(nonface_path, '%d' % (int(l)+1)))
    #end non faces

    #---------------------------------------------------------------------------------------------------


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:d:c:o:", ["help", "data=", "converted=", "output="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    if len(opts) < 3:
        usage()
        sys.exit(2)
    output_dir = None
    data_dir = None
    converted_dir = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--data"):
            data_dir = a
        elif o in ("-c", "--converted"):
            converted_dir = a
        elif o in ("-o", "--output"):
            output_dir = a
        else:
            assert False, "unhandled option"
    print 'Image feature extraction'
    t0 = time.time()
    data = get_image_features(data_dir)
    t1 = time.time()
    print '----',t1-t0,'s ----'
    print 'face detection'
    t0 = time.time()
    idx = partition_faces(data_dir, converted_dir, output_dir)
    t1 = time.time()
    print '----',t1-t0,'s ----'
    print 'clustering faces'
    t0 = time.time()
    cluster_faces(data, idx, output_dir)
    t1 = time.time()
    print '----',t1-t0,'s ----'
    print 'clustering non faces'
    t0 = time.time()
    cluster_nonfaces(data, idx, output_dir)
    t1 = time.time()
    print '----',t1-t0,'s ----'
    print 'video classifiers'
    t0 = time.time()
    videoOutput_dir = os.path.join(output_dir, 'nonface')
    videoClassifier.videoprocessor(data_dir, converted_dir, videoOutput_dir)
    t1 = time.time()
    print '----',t1-t0,'s ----'
    print 'DONE!!!'


if __name__ == '__main__':
    main(sys.argv)