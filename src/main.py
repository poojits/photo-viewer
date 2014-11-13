#!/usr/bin/env python
import cv2
import rgb

num_files = 150
for n in range(1, num_files+1):
    print 'Opening file %d' % n
    filename = 'data/image%03d.rgb' % n
    img = rgb.imread(filename)
    cv2.imshow('RGB Image', img)
    cv2.waitKey(100)
    cv2.imwrite('data/image%03d.png'%n, img)