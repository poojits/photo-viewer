photo-viewer
============

Installation
===============
1. Make sure to have ```OpenCV 2.4.9, numpy, scikit-learn``` installed.
2. Put your ```.rgb``` data files in a folder ```photo-viewer/data/```
3. ```cd photo-viewer/src/```
4. Run ```python rgb_converter.py -i ../data/ -o ../converted```
5. Run ```python main.py -d ../data/ -c ../converted/ -o ../clusters```
6. ```cd ..```
7. Now the ```clusters/``` directory contains your clusters.
8. Run ```npm install``` to install the node dependencies.
9. Run ```npm start``` to load the application.
