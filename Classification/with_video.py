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
# Run classification from a live stream on a website
# python3 with_video.py -a https://www.youtube.com/watch?v=21X5lGlDOfg
#
# https://www.earthcam.com/world/england/london/abbeyroad/?cam=abbeyroad_uk
# https://www.earthcam.com/usa/washington/seattle/?cam=seattleskyline


import cv2
import sys
import time
import imutils
import argparse
import numpy as np
import ffmpeg_streaming
from imutils.video import VideoStream
import m3u8
import streamlink
import urllib
from threading import Thread


####################
#
# Pass the output video to our server / display output frames
#
####################

def output(frame):
    cv2.imshow("Output Stream", frame)
    cv2.waitKey(1) & 0xFF


####################
#
# Pass the frames to our classification / detection models
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
    check, frame = vs.read()
    if not check or not vs.isOpened():
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
        output(frame)
    vs.release()
    cv2.destroyAllWindows()





"""
def get_live_stream(url):
    print("Getting live stream")
    stream = streamlink.streams(url)
    stream_url = stream["best"]
    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]


def read_live_stream(url):
    chunks = 16
    for i in range(chunks):
        stream_seg = get_live_stream(url)
        print("Reading live stream")
        #vs_file = open("live_stream.ts", 'ab+')
        with urllib.request.urlopen(stream_seg.uri) as response:
            vs_file = open("live_stream.ts", 'ab')
            html = response.read()
            vs_file.write(html)
            print("Getting frames")
            vs = cv2.VideoCapture(vs_file)
            stream_from_source(vs)
            #stream_from_source(html)


#######
from threading import Thread
class RTSPVideoWriterObject(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
        self.output_video = cv2.VideoWriter('output.avi', self.codec, 30, (self.frame_width, self.frame_height))

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Display frames in main program
        if self.status:
            cv2.imshow('frame', self.frame)

        # Press Q on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save obtained frame into video output file
        self.output_video.write(self.frame)


rtsp_stream_link = "https://www.earthcam.com/usa/washington/seattle/?cam=seattleskyline"
video_stream_widget = RTSPVideoWriterObject(rtsp_stream_link)
while True:
    try:
        video_stream_widget.show_frame()
        #video_stream_widget.save_frame()
    except AttributeError:
        pass

#######
"""



from threading import Thread
import cv2, time

class ThreadedCamera(object):
    def __init__(self, src=0):
        print("init")
        self.vs = cv2.VideoCapture(src)
        #self.vs.set(cv2.CAP_PROP_FOURCC, 2)
        #self.vs.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.thread = Thread(target=self.update, args=())

        #self.FPS = 1/30
        #self.FPS_MS = int(self.FPS * 1000)

        #self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.frame = None
        self.status = False

    def update(self):
        print("update")
        while True:
            if self.vs.isOpened():
                print("reading frame")
                (self.status, self.frame) = self.vs.read()
            #time.sleep(self.FPS)

    def get_frame(self):
        print("get_frame")
        if self.status:
            return self.frame
        print("frame is none")
        return None

    def show_frame(self):
        cv2.imshow('frame', self.frame)
        cv2.waitKey(self.FPS_MS)


url = "https://www.youtube.com/watch?v=21X5lGlDOfg"
#url = "https://www.earthcam.com/world/england/london/abbeyroad/?cam=abbeyroad_uk"
#threaded_camera = ThreadedCamera(url)
stream = ThreadedCamera(url)
time.sleep(2.0)
while True:
    #try:
        #threaded_camera.show_frame()
    #except AttributeError:
        ##print("Err")
        #sys.exit()
    frame = stream.get_frame()
    if frame is not None:
        cv2.imshow("Context", frame)
        cv2.waitKey(1)
    else:
        print("Err: frame is none")
        sys.exit()



sys.exit()


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
    vs = cv2.VideoCapture(0)
    time.sleep(2.0)
    stream_from_source(vs)

elif args["filepath"] is not None:
    vs = cv2.VideoCapture(args["filepath"])
    stream_from_source(vs)

elif args["address"] is not None:
    #vs = ffmpeg_streaming.input(args["address"])
    #vs = get_live_stream(args["address"])
    #vs = streamlink.streams(args["address"])
    #vs = cv2.VideoCapture(vs)
    #read_live_stream(args["address"])
    print("Getting live stream")
    cap = cv2.VideoCapture()
    vs = cap.open(args["address"])
    stream_from_source(vs)

'''try:
    stream_from_source(vs)
except:
    sys.exit()'''



##
