#!/usr/bin/env python
import cv2
import rgb
import numpy as np
import os
import shutil
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
from timeit import itertools

def mymkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

#-------------------------constructing histograms-------------------------------        
num_files = 300
data = []        
for n in range(1, num_files+1):
    filename = 'data/image%03d.rgb' % n
    rgb_image = rgb.imread(filename)
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv_image], [0,1,2], None, [8,8,8], [0,180,0,256,0, 256])
    hist = cv2.normalize(hist).flatten()
    data.append(hist)
#---------------------------------------------------------------------------------  

#-----------------------------FACE/NON-FACE----------------------------------
#path for haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
idx = [] 
shutil.rmtree('face/')
shutil.rmtree('nonface/')
mymkdir('face')
mymkdir('nonface')
for n in range(1, num_files+1):
    filename = 'data/image%03d.rgb' % n
    img = rgb.imread(filename)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image,1.2,2)
    if len(faces):
        idx.append(1)
        shutil.copy2('data/image%03d.png' % n, 'face/' )
    if not len(faces):
        idx.append(2)
        shutil.copy2('data/image%03d.png' % n, 'nonface/' )
#print idx.count(1)
#print idx.count(2)

#--------------------------------------------------------------

#------------------CLUSTERING OF FACES--------------------------

#faces
modified_data = []
fileindex = []
for n in range(0, num_files):
    if(idx[n]==1):
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
for l in range(1, K+1):
    mymkdir('face/%d' % l)
for i, l in enumerate(label):
    shutil.copy2('data/image%03d.png' % (fileindex[i]+1), 'face/%d/'%(int(l)+1))
#end_faces
#-------------------------------------------------------------------------------------------------


#-------------------------CLUSTERING NON FACES----------------------------------------------------
#non faces    
modified_data = []
fileindex = []
for n in range(0, num_files):
    if(idx[n]==2):
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
for l in range(1, K+1):
    mymkdir('nonface/%d' % l)
for i, l in enumerate(label):
    shutil.copy2('data/image%03d.png' % (fileindex[i]+1), 'nonface/%d/'%(int(l)+1))
#end non faces

#---------------------------------------------------------------------------------------------------