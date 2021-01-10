# MOT-Live-Streaming
This is MOT task with live streaming.

## HW4 Grading
1. Base Model (40%): video/audio live steaming
2. Function 1 (30%): video live streaming with object tracking
3. Function 2 (10%): Providing a user interface to specify which object to track
4. Report (20%)
5. Bonus (10%): supporting multiple bitrates OR trick mode (users can perform
pause/resume/rewind)

## TODO
To create live streaming with MPEG-DASH, you will need to
* Use webcam to capture/encode live video
* Use your deep learning network model to do segmentation or object tracking
* Use ffmpeg to transcode the video into .mp4
* Use MP4Box with a live profile (there are two profiles supported: live and onDemand) to generate
fragmented mp4 and a .mpd file
* Create HTML file to play the video (or with controls such as play, pause)
* View the results in a browser that supports HTML5.


## Requirements
### Python Packages
* Flask
* motmetrics
* [cython_bbox](https://blog.csdn.net/qq_19707521/article/details/106692395)
### Others
* [MP4Box](https://gpac.wp.imt.fr/downloads/)
* ffmpeg

## Main Files
* camera_tracking.py : load camera and track people
* track.py : main for tracking, saving frames, and generating mpdfile
* visualization.py : plot the tracked bboxs on frames
* app.py : main for Flask

## Usages
* camera tracking on local
```python camera_tracking.py --weights weights/jde.1088x608.uncertainty.pt```

* run flask, and access [127.0.0.1:5000](127.0.0.1:5000).
```Flask run```

* generate mpd file (sample example)
```MP4Box -dash 1000 -profile dashavc264:live -bs-switching multi <source.mp4>```

## Problems
* The video output by ```cv2.VideoWriter_fourcc(*'MP4')``` is not supported by HTML. 
+ [Solution](https://stackoverflow.com/questions/49530857/python-opencv-video-format-play-in-browser): get OpenH264 library

* Due to cache of Flask, mpd file will not update