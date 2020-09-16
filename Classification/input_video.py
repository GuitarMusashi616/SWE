# Ty Bergstrom
# input_video.py
# CSCE A401
# September 2020
# Software Engineering Project
#
# Trying out different sources of input video
# For running detections and classification with our ML models
#
# With a webcam or other device
# $ python3 input_video.py -d tru
#
# From a video file upload
# # $ python3 input_video.py -f path/to/video/file.mp4
#
# From a youtube livestream
# $ python3 input_video.py -y https://www.youtube.com/watch?v=21X5lGlDOfg
#
# Other urls livestreams are not supported
#
# Enter 'q' to quit the video after it starts playing
# Keep hitting 'q' if it keeps playing


import cv2
import sys
import time
import imutils
import argparse
import numpy as np
from vidgear.gears import CamGear


####################
#
# Pass the output video to our server / display output frames
#
####################


def output(frame):
    frame = imutils.resize(frame, width=500)
    cv2.imshow("Output Stream", frame)
    cv2.waitKey(1) & 0xFF


####################
#
# Pass the frames to our ML classification and detection models
#
####################


def detect(frame):
    return frame


####################
#
# Get frames from video source
#
####################


def check_source(vs):
    print("Checking source")
    check, frame = vs.read()
    if not check or not vs.isOpened():
        print("No video source found")
        sys.exit()


def still_reading(frame):
    if frame is None:
        return 0
    if cv2.waitKey(1) == ord('q'):
        return 0
    return 1


def quit(vs):
    print("Quitting successfully")
    cv2.destroyAllWindows()
    sys.exit()


def stream_from_source(vs):
    check_source(vs)
    print("Reading video stream")
    while True:
        check, frame =  vs.read()
        if not still_reading(frame) or not check:
            break
        frame = detect(frame)
        output(frame)
    vs.release()
    quit(vs)


def livestream(vs):
    print("Reading livestream")
    while True:
        frame = vs.read()
        if not still_reading(frame):
            break
        frame = detect(frame)
        output(frame)
    vs.stop()
    quit(vs)


####################
#
# Set-up
#
####################


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--device", default=False)
ap.add_argument("-f", "--filepath", default=None)
ap.add_argument("-y", "--youtube", default=None)
args = vars(ap.parse_args())

if args["device"]:
    print("Preparing device")
    vs = cv2.VideoCapture(0)
    time.sleep(2.0)
    stream_from_source(vs)

elif args["filepath"] is not None:
    print("Loading video file")
    vs = cv2.VideoCapture(args["filepath"])
    stream_from_source(vs)

elif args["youtube"] is not None:
    print("Loading youtube livestream")
    vs = CamGear(source=args["youtube"], y_tube=True).start()
    livestream(vs)
else:
    print(":/")



##
