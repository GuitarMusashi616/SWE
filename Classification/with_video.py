# Ty Bergstrom
# with_video.py
# CSCE A401
# September 2020
# Software Engineering Project
#
# Trying out running detections and classification with
# different sources of input video
#
# Run classification with a webcam or other device
# $ python3 with_video.py -d tru
#
# Run classification from a video file upload
# # $ python3 with_video.py -f path/to/video/file.mp4
#
# Run classification from a live stream
# python3 with_video.py -a "https://www.youtube.com/watch?v=21X5lGlDOfg"


import cv2
import sys
import imutils
import argparse
import numpy as np
import ffmpeg_streaming
from imutils.video import VideoStream


####################
#
# Pass the output video to our server / display output frames
#
####################

def output(frame):
    return None


####################
#
# Pass the frames to our classification / detection models
#
####################

def detect(frame):
    return None


####################
#
# Get frames from video source
#
####################

def check_source(vs):
    check, frame = vs.read()
    if not check:
        print("No video source found")
        sys.exit()


def still_reading(check):
    if not check:
        return 0
    if cv2.waitKey(1) == ord('q'):
        return 0
    return 1


def stream_from_source(vs):
    check_source(vs)
    while True:
        check, frame =  vs.read()
        if not still_reading(check):
            break
        frame = imutils.resize(frame, width=500)
        frame = detect(frame)
        frame = output(frame)
    vs.release()
    cv2.destroyAllWindows()


####################
#
# Set-up
#
####################

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--device", default=False)
ap.add_argument("-f", "--filepath", default=None)
ap.add_argument("-a", "--address", default=None)
args = vars(ap.parse_args())

if args["device"]:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

elif args["file"] is not None:
	vs = cv2.VideoCapture(args["filepath"])

elif args["address"] is not None:
	vs = ffmpeg_streaming.input(args["address"])

try:
    stream_from_source(vs)
except:
    sys.exit()



##
