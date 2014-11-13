#!/usr/bin/env python
import numpy as np
__author__ = "Poojit Sharma"

def imread(filepath, height=288, width=352, n_channels=3):
    """Read an image from byte array stored as RRRGGGBBB"""
    raw_data = np.fromfile(filepath, dtype='uint8')
    img = np.zeros((height, width, n_channels), np.uint8)
    pixels = width * height
    # Assign the red channel
    img[:, :, 2] = raw_data[0:pixels].reshape((height, width))
    # Assign the green channel
    img[:, :, 1] = raw_data[pixels:2*pixels].reshape((height, width))
    # Assign the blue channel
    img[:, :, 0] = raw_data[2*pixels:3*pixels].reshape((height, width))
    return img
