photo-viewer
============

Installation
===============
1. Make sure to have ```OpenCV 2.4.9 with ffmpeg support (theora codec), numpy, scipy, scikit-learn, nodejs, npm``` installed.
2. Put your ```.rgb``` data files in a folder ```photo-viewer/data/```
3. ```cd photo-viewer/src/```
4. Run ```python rgb_converter.py -i ../data/ -o ../converted```
5. Run ```python main.py -d ../data/ -c ../converted/ -o ../public/images/clusters```
6. ```cd ..```
7. Now the ```public/images/clusters/``` directory contains your clusters with the ```png``` images files and ```ogv``` video files, which can then be rendered in the browser.
8. Run ```npm install``` to install the node dependencies, including node-webkit.
9. Run ```npm start``` to load the application.

Photo-viewer for dummies
========================
After running the application, click on the image/video tiles to open that cluster and browse.

Team
=====
```
Poojit Sharma           poojitsh@usc.edu    4458-4340-25
Bhargav Venkataraman    bhargavv@usc.edu    6658-3128-87
Sandeep Thippeswamy 	thippesw@usc.edu    3819-4035-78
```
