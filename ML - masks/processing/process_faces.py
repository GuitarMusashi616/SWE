# Ty Bergstrom
# process_faces.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Input original images
# Detect and extract a face or faces from an image
# Save each face as a new 256x256 image (originals are not overwritten)
#
# This is for if the models need good photos of just faces and
# need to exclude everything else from an image.
# Make sure to check the processed dataset afterwords and
# delete any images that aren't actually a face.
#
# Other notes:
# This outputs some info to a file named double_take_idx.txt
# It will contain a list of original file paths for any images that did not find a face.
# To help find images that you need to go back and manually process.
#
# python3 process_faces.py -d mask
# python3 process_faces.py -d without_mask -o tru


from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True)
ap.add_argument("-o", "--one", type=bool, default=False)
args = vars(ap.parse_args())

originals_dir = "../original_dataset/"
proto = "../face_detector/deploy.prototxt"
model = "../face_detector/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(proto, model)
threshold = 0.8 # a probability threshold to decrease false positives
dataset = args["dataset"]
img_paths = sorted(list(paths.list_images(originals_dir + dataset)))
total_saved = 0 # how many total faces from the entire dataset
double_take = [] # images with zero faces saved that you will have to manually process if you want their face
# Save time if you know there is only one face per img,
# Or if you only want to get the one face with the highest probability of being an actual face
one_photo_per_img = args["one"]
f = open("double_take_idx.txt","a+")
print("processing:", len(img_paths), "input images...")

for (itr, img_path) in enumerate(img_paths):
	name = img_path.split(os.path.sep)[-2]
	image = cv2.imread(img_path)
	(h, w) = image.shape[:2]

	# detect faces in the image
	imageBlob = cv2.dnn.blobFromImage(cv2.resize(image,
	(300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0),
	swapRB=False, crop=False)
	detector.setInput(imageBlob)
	detections = detector.forward()

	total_saved_per_img = 0

	if len(detections) < 1:
		double_take.append(img_path)
		break
	else:
		img_itr = 0 # append to the save filepath if more than one face per photo
        # Loop through all detected faces
		for i in range(0, detections.shape[2]):
			if one_photo_per_img:
    			# Get only the one face that was detected with highest probability
				i = np.argmax(detections[0, 0, :, 2])
			confidence = detections[0, 0, i, 2]
            # Only bother with faces over the threshold for true positives
			if confidence > threshold:
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				if startY - 32 > 0:
					startY -= 32
				if startX - 32 > 0:
					startX -= 32
				face = image[startY:endY+32, startX:endX+32]
				(fH, fW) = face.shape[:2]
				if fW < 64 or fH < 64:
					continue
				face = imutils.resize(face, width=256, height=256)
				filename = "../processed_dataset/" + dataset + "/" + str(itr+1) + "_" + str(img_itr) + ".jpg"
				cv2.imwrite(filename, face)
				total_saved += 1
				total_saved_per_img += 1
				img_itr += 1
				if one_photo_per_img:
					break
	if total_saved_per_img == 0:
		double_take.append(img_path)


print(total_saved, "total saved faces images")
if len(double_take) > 0:
	f.write(originals_dir + dataset)
	f.write("\nZero faces were saved from these images: \n")
	for img_path in double_take:
		print(img_path)
		f.write(img_path)
		f.write("\n")
f.close()



##
