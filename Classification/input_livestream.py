# Ty Bergstrom
# input_livestream.py
# CSCE A401
# September 2020
# Software Engineering Project
#
# Trying out getting a livestream as video input
#
# $ python3 input_livestream.py -u https://www.youtube.com/watch?v=21X5lGlDOfg


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

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", default=None)
args = vars(ap.parse_args())

url = args["url"]

#try_impl = 1
#try_impl = 2
#try_impl = 3
#try_impl = 4
#try_impl = 5
#try_impl = 6
try_impl = 7


############
#
# One implementation
#
############

# The basic idea is downloading the stream in chunks and saving the chunks.
# Then reading the chunks as you would normally read video from file.
# But I think it's meant for just saving a stream and not working with it simultaneously.
# Maybe it would work with multi-threading

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

# Seems like the intuitive way of reading frames from the livestream and
# always updating the current frame with a while true loop.
# But I think the issue is that cv2.VideoCapture() doesn't work for live streams.

from threading import Thread

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
# Do it with ffmpeg which requires some weird ffmpeg stuff

from ffmpeg_streaming import Formats

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
# This looks pretty cool
# Multi-threading upload while downloading
# https://flashphoner.com/how-to-grab-a-video-from-youtube-and-share-it-via-webrtc-in-real-time/

import subprocess

def dwnld_livestream(url, stream_id, destination):
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



############
#
# A fifth implementation
#
############

import pafy

def pafy_livestream(url):
    p = pafy.new(url)
    best = p.getbest(preftype="webm")
    vs = cv2.VideoCapture()
    vs.open(best.url)
    while True:
        frame = vs.read()
        cv2.imshow("Output Stream", frame)
        cv2.waitKey(1) & 0xFF

if try_impl == 5:
    pafy_livestream(url)



############
#
# A sixth implementation
#
############

# This actually works but only with youtube livestreams

from vidgear.gears import CamGear

def vidgear_livestream(url):
    vs = CamGear(
        source=url,
        y_tube=True
    ).start()
    while True:
        frame = vs.read()
        if frame is None:
            break
        frame = imutils.resize(frame, width=500)
        cv2.imshow("Output Stream", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

if try_impl == 6:
    vidgear_livestream(url)



############
#
# This obviously never worked either, maybe just a simple error?
#
############

def vidcap(url):
    vs = cv2.VideoCapture(url)
    while True:
        frame = vs.read()
        cv2.imshow("Output Stream", frame)
        cv2.waitKey(1) & 0xFF

if try_impl == 7:
    vidcap(url)



##
