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

num_files = 300


def usage():
    msg = '''Usage: python main.py -d <data directory> -c <converted data directory> -o <output directory>'''
    print msg


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
        faces = face_cascade.detectMultiScale(gray_image, 1.2, 2)
        png_path = os.path.join(converted_dir, 'image%03d.png' % n)
        if len(faces):
            idx.append(1)
            shutil.copy2(png_path, face_path)
        if not len(faces):
            idx.append(2)
            shutil.copy2(png_path, nonface_path)
    #print idx.count(1)
    #print idx.count(2)
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

    #print len(modified_data)
    #print len(fileindex)
    print idx.count(1)

    # data is num_files x 64
    criteria = (cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 7
    connectivity = kneighbors_graph(modified_data, n_neighbors=3)
    ward = AgglomerativeClustering(n_clusters=7, connectivity=connectivity,
                                   linkage='ward').fit(np.array(modified_data))
    #ward = AgglomerativeClustering(n_clusters=K, linkage='ward').fit(np.array(data))
    #ret, label, center = cv2.kmeans(np.array(data), K, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    label = ward.labels_
    face_path = os.path.join(output_dir, 'face')
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

    #print len(modified_data)
    #print len(fileindex)
    print idx.count(2)

    # data is num_files x 64
    criteria = (cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 8
    connectivity = kneighbors_graph(modified_data, n_neighbors=3)
    ward = AgglomerativeClustering(n_clusters=8, connectivity=connectivity,
                                   linkage='ward').fit(np.array(modified_data))
    #ward = AgglomerativeClustering(n_clusters=K, linkage='ward').fit(np.array(data))
    #ret, label, center = cv2.kmeans(np.array(data), K, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    label = ward.labels_
    nonface_path = os.path.join(output_dir, 'nonface')
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
    data = get_image_features(data_dir)
    idx = partition_faces(data_dir, converted_dir, output_dir)
    cluster_faces(data, idx, output_dir)
    cluster_nonfaces(data, idx, output_dir)

if __name__ == '__main__':
    main(sys.argv)