# Ty Bergstrom
# input_livestream.py
# CSCE A401
# September 2020
# Software Engineering Project
#
# python3 input_livestream.py -u https://www.youtube.com/watch?v=21X5lGlDOfg
#
# Trying out getting a livestream as video input


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
import subprocess
from ffmpeg_streaming import Formats

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", default=None)
args = vars(ap.parse_args())

url = args["url"]

#try_impl = 1
try_impl = 2
#try_impl = 3
#try_impl = 4


############
#
# One implementation
#
############

# The basic idea is downloading the stream in chunks and saving the chunks.
# Then reading the chunks as you would normally read video from file.
# But I think this is meant for just saving a stream and not working with it.
# So just need to try adjusting it with multithreading.

def get_livestream(url):
    print("Getting live stream")
    stream = streamlink.streams(url)
    stream_url = stream["best"]
    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]

def read_livestream(url):
    chunks = 16
    for i in range(chunks):
        stream_seg = get_livestream(url)
        print("Reading live stream")
        #vs_file = open("live_stream.ts", 'ab+')
        with urllib.request.urlopen(stream_seg.uri) as response:
            vs_file = open("live_stream.ts", 'ab')
            html = response.read()
            vs_file.write(html)
            print("Getting frames")
            vs = cv2.VideoCapture(vs_file)
            #vs = cv2.VideoCapture(html)

if try_impl == 1:
    read_livestream(url)



############
#
# Another implementation
#
############

# It seems like the intuitive way of reading frames from the livestream and
# always updating the current frame with a while true loop.
# But I think the issue is that cv2.VideoCapture() is not meant for live streams.

class live_stream(object):
    def __init__(self, src):
        print("init")
        self.vs = cv2.VideoCapture(src)
        #self.vs.set(cv2.CAP_PROP_FOURCC, 2)
        #self.vs.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.vs.set(cv2.CAP_PROP_POS_FRAMES, 2)
        #self.FPS = 1/30
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.frame = None
        self.status = False

    def update(self):
        while True:
            if self.vs.isOpened():
                (self.status, self.frame) = self.vs.read()
            #time.sleep(self.FPS)

    def get_frame(self):
        if self.status:
            return self.frame
        return None

    def show_frame(self):
        cv2.imshow('frame', self.frame)
        cv2.waitKey(self.FPS_MS)

def read_from_live_stream(url):
    stream = live_stream(url)
    time.sleep(2.0)
    while True:
        frame = stream.get_frame()
        if frame is not None:
            cv2.imshow("Context", frame)
            cv2.waitKey(1)
        else:
            continue

if try_impl == 2:
    read_from_live_stream(url)



############
#
# A third implementation
#
############

# todo
# Do it with ffmpeg which requires some weird stuff

def ffmpeg_livestream(url):
    video = ffmpeg_streaming.input(url)
    hls = video.hls(Formats.h264())
    hls.auto_generate_representations([480])
    hls.fragmented_mp4()
    hls.output("hls.m3u8")


if try_impl == 3:
    ffmpeg_livestream(url)



############
#
# A fourth implementation
#
############

# todo
# This is actually pretty cool
# https://flashphoner.com/how-to-grab-a-video-from-youtube-and-share-it-via-webrtc-in-real-time/



def dwnld_livestream(url, stream_id, destination)
    _youtube_process = subprocess.Popen(
        ('youtube-dl','-f','','--prefer-ffmpeg',
        '--no-color', '--no-cache-dir', '--no-progress',
        '-o', '-', '-f', '22/18', url, '--reject-title',
        stream_id), stdout=subprocess.PIPE
    )
    _ffmpeg_process = subprocess.Popen(
        ('ffmpeg', '-re', '-i', '-', '-preset', 'ultrafast',
        '-vcodec', 'copy', '-acodec', 'copy', '-threads',
        '1', '-f', 'flv', destination + "/" + stream_id),
        stdin=_youtube_process.stdout
    )

if try_impl == 4:
    dwnld_livestream(url, "output", "https://...")



##
