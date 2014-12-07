#!/usr/bin/env python
import cv2
import rgb
import numpy as np
import os
import shutil
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

def mymkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


num_files = 150
data = []
for n in range(1, num_files+1):
    filename = 'data/image%03d.rgb' % n
    rgb_image = rgb.imread(filename)
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist).flatten()
    data.append(hist)

# data is num_files x 64
criteria = (cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 6
connectivity = kneighbors_graph(data, n_neighbors=3)
ward = AgglomerativeClustering(n_clusters=6, connectivity=connectivity,
                               linkage='ward').fit(np.array(data))
#ward = AgglomerativeClustering(n_clusters=K, linkage='ward').fit(np.array(data))
#ret, label, center = cv2.kmeans(np.array(data), K, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
label = ward.labels_
for l in range(1, K+1):
    mymkdir('%d' % l)
for i, l in enumerate(label):
    shutil.copy2('data/image%03d.png' % (int(i)+1), '%d/'%(int(l)+1))