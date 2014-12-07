#!/usr/bin/env python
import numpy as np
import cv2

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

def vdread(filepath, height=288, width=352, n_channels=3):
    """Read an video from byte array stored as RRRGGGBBB"""
    raw_data = np.fromfile(filepath, dtype='uint8')
    n_frames = len(raw_data) / (height*width*n_channels)
    video = np.zeros((n_frames, height, width, n_channels), np.uint8)
    pixels = width * height
    for i in range(0, n_frames):
        offset = i*pixels*3
        # Assign the red channel
        video[i, :, :, 2] = raw_data[offset:(offset+pixels)].reshape((height, width))
        # Assign the green channel
        video[i, :, :, 1] = raw_data[offset+pixels:(offset+2*pixels)].reshape((height, width))
        # Assign the blue channel
        video[i, :, :, 0] = raw_data[(offset+2*pixels):(offset+3*pixels)].reshape((height, width))
    return video
def is_image(filepath, height=288, width=352, n_channels=3):
    """Read an image from byte array stored as RRRGGGBBB"""
    raw_data = np.fromfile(filepath, dtype='uint8')
    if len(raw_data) > (height*width*n_channels):
        return False
    else:
        return True

def is_video(filepath, height=288, width=352, n_channels=3):
    return not is_image(filepath, height, width, n_channels)