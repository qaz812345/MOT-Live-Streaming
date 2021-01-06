# MOT-Live-Streaming
This is MOT task with live streaming.

## Requirements
### Python Packages
* Flask
* motmetrics
* [cython_bbox](https://blog.csdn.net/qq_19707521/article/details/106692395)
### Others
* [MP4Box](https://gpac.wp.imt.fr/downloads/)

## Main Files
* camera_tracking.py : load camera and track people
* track.py : main code for tracking and saving frames
* visualization.py : plot the tracked bboxs on frames
* app.py : main for Flask

## Usages
* camera tracking on local
```python camera_tracking.py --weights weights/jde.1088x608.uncertainty.pt```

* run flask, and access [127.0.0.1:5000](127.0.0.1:5000)
```Flask run```

* generate mpd file
```MP4Box -dash 1000 -profile dashavc264:live -bs-switching multi <source.mp4>```