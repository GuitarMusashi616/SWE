# Ty Bergstrom
# lowerq.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Take a dataset of faces cropped from higher quality images.
# Process them to look like crops from low quality video streams.
# So then you can have a dataset of faces similar to how they appear in video.
#
# -o full/path/to/input/original/dataset -p full/path/to/output/processed/dataset
# $ python3 lowerq.py -o ../data/lowerq_dataset -p ../data/lowerq_processed
#
# It should be a prepared dataset that's ready to train after this processing.
# Then you can test the model and if it's not as accurate you can run this again,
# And increase or decrease the parameters to see which improves the accuracy.


import numpy as np
from imutils import paths
import argparse
import cv2
import sys
import os

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--original", required=True)
ap.add_argument("-p", "--processed", required=True)
args = vars(ap.parse_args())

original_dir = args["original"]
processed_dir = args["processed"]

img_paths = sorted(list(paths.list_images(original_dir)))

# How much pixelation
pix_L = 64 # Very light
pix_M1 = 42 # Medium
pix_M2 = 32 # Medium
pix_H = 16 # Very heavy

pix = pix_M2

# How much blur, kernel size
blr_M = 5 # Medium
blr_H = 9 # Heavy

blr = blr_H

if len(img_paths) < 1:
	print("Err: The directory", original_dir, "was empty")
	sys.exit(1)

def smooth(img, b):
	kernel = np.ones((b,b), np.float32) / (b*b)
	img = cv2.filter2D(img, -1, kernel)
	return img

def blur(img, b):
	img = cv2.GaussianBlur(img, (b,b), cv2.BORDER_DEFAULT)
	return img

def pixelate(img, p):
	(h, w) = img.shape[:2]
	img = cv2.resize(img, (p, p), interpolation=cv2.INTER_LINEAR)
	img = cv2.resize(img, (h, w), interpolation=cv2.INTER_NEAREST)
	return img

def blur_first(img, b, p):
	img = blur(img, b)
	img = pixelate(img, p)
	return img

def pix_first(img, p, b):
	img = pixelate(img, p)
	img = blur(img, b)
	return img

def save_n_rename(img, processed_dir, img_path, it):
	basename = os.path.basename(img_path)
	filename, ext = os.path.splitext(basename)
	img_path = processed_dir + "/" + filename + "_" + str(it) + ext
	cv2.imwrite(img_path, img)

for img_path in img_paths:
	img = cv2.imread(img_path)
	img = blur_first(img, blr, pix)
	img = pix_first(img, pix, blr)
	save_n_rename(img, processed_dir, img_path, 0)
	img = cv2.imread(img_path)
	img = pix_first(img, pix, blr)
	img = blur_first(img, blr, pix)
	save_n_rename(img, processed_dir, img_path, 1)



##
