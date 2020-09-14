



# $ python3 lowerq.py -o ../data/lowerq_dataset -p ../data/lowerq_processed

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
pix_L = 4 # Very light
pix_M = 8 # Medium
pix_H = 16 # Very heavy

pix = pix_M

# How much blur
blr_M = 5 # Medium
blr_H = 9 # Heavy

blr = blr_M

if len(img_paths) < 1:
	print("Err: The directory", original_dir, "was empty")
	sys.exit(1)

def blur(img, b):
	img = cv2.GaussianBlur(img, (b,b), cv2.BORDER_DEFAULT)
	return img

def pixelate(img, p):
	(h, w) = img.shape[:2]
	(pix_h, pix_w) = (int(h/p), int(w/p))
	print(pix_h, pix_w)
	img = cv2.resize(img, (pix_h, pix_w), interpolation=cv2.INTER_LINEAR)
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
	img1 = blur_first(img, blr, pix)
	img1 = pix_first(img1, pix, blr)
	save_n_rename(img1, processed_dir, img_path, 0)
	img2 = pix_first(img, pix, blr)
	img2 = blur_first(img2, blr, pix)
	save_n_rename(img2, processed_dir, img_path, 1)



##
