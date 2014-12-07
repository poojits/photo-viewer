#!/usr/bin/env python
import rgb
import os
import sys
import getopt
import cv2
import string
import numpy as np

def usage():
    msg = '''Usage: python rgb_converter.py -i <input directory> -o <output directory>'''
    print msg

def convert_data(input_dir, output_dir):
    all_files = [ f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith('.rgb')]
    num_files = len(all_files)
    mymkdir(output_dir)
    for f in all_files:
        filepath = os.path.join(input_dir, f)
        print 'Processing ' + filepath
        if rgb.is_image(filepath):
            img = rgb.imread(filepath)
            png_filename = string.replace(f, '.rgb', '.png')
            png_filepath = os.path.join(output_dir, png_filename)
            cv2.imwrite(png_filepath, img)
        else:
            video = rgb.vdread(filepath)
            video_filename = string.replace(f, '.rgb', '.mp4')
            video_filepath = os.path.join(output_dir, video_filename)
            video_writer = cv2.VideoWriter(video_filepath, cv2.cv.FOURCC('m', 'p', '4', 'v'), 30, (352, 288), True)
            for frame in video:
                video_writer.write(frame)
            video_writer.release()

def mymkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def folder_exists(folder_path):
    return folder_path is not None and os.path.isdir(folder_path)

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:i:o:", ["help", "input=", "output="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    if len(opts) < 2:
        usage()
        sys.exit(2)
    output_dir = None
    input_dir = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output_dir = a
        elif o in ("-i", "--input"):
            input_dir = a
        else:
            assert False, "unhandled option"
    convert_data(input_dir, output_dir)

if __name__ == '__main__':
    main(sys.argv) 