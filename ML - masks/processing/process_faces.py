# Ty Bergstrom
# process_faces.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Input original images
# Detect and extract a face or faces from an image
# Save each face as a new 256x256 image (originals are not overwritten)
# Find them in the directory processed_dataset/
#
# This is for if the models need good photos of just faces and
# need to exclude everything else from an image.
# Make sure to check the processed dataset afterwords and
# delete any images that aren't actually a face,
# or later you can manually crop the faces on any that aren't perfect
#
# Other notes:
# This outputs some info to a file named double_take_idx.txt
# Including a list of original file paths for any images that did not find a face.
# To help find images that you need to go back and manually process.
# Also, copies of those files are saved to processed_dataset/double_take/
# So that you can find and manually process those images much quicker.
#
# This is set up to only process one directory at a time, there's a good reason.
# Use preprocess.sh to run this on each directory that you need
# "--originals_dir" is the parent directory of the entire project dataset
# "--dataset" is the directory of one of the classes for the project
#
# python3 process_faces.py -d mask
# python3 process_faces.py -d without_mask -o tru
# But it's better run run from a script for consistency

# The -o arg is to limit each image to extract only one face


from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import sys
import os


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True)
ap.add_argument("-o", "--originals_dir", default="../data/original_dataset/")
ap.add_argument("-p", "--processed_dir", default="../data/processed_dataset/")
ap.add_argument("-n", "--one", type=bool, default=False)
args = vars(ap.parse_args())

# Face detection stuff
proto = "../face_detector/deploy.prototxt"
model = "../face_detector/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(proto, model)
threshold = 0.8 # A probability threshold to increase detections or decrease false positives

processed_dir = args["processed_dir"]
originals_dir = args["originals_dir"]
dataset = args["dataset"]

img_paths = sorted(list(paths.list_images(originals_dir + dataset)))

if len(img_paths) < 1:
	print("Err: The directory", originals_dir + dataset, "was empty")
	sys.exit(1)

total_saved = 0 # How many total faces were extracted from the dataset
double_take = [] # List of images with zero faces extracted, they will need to be manually processed
f = open("double_take_idx.txt","a+") # Save a log of files that you need to go back & manually process
one_photo_per_img = args["one"] # Save time if you know there is only one face per img in the dataset
HXW = 256

print("processing:", len(img_paths), "input images from", originals_dir + dataset)


for (itr, img_path) in enumerate(img_paths):
	image = cv2.imread(img_path)
	(h, w) = image.shape[:2]

	# Detect faces in the image
	img_blob = cv2.dnn.blobFromImage(
		cv2.resize(image, (300, 300)),
		1.0, (300, 300),
		(104.0, 177.0, 123.0),
		swapRB=False, crop=False
	)
	detector.setInput(img_blob)
	detections = detector.forward()

	# Append this iterator to the save filepath if more than one face per image
	img_itr = 0

    # Loop through all detected faces in the image
	for i in range(0, detections.shape[2]):
		if one_photo_per_img:
			# Get only the one face that was detected with highest probability
			i = np.argmax(detections[0, 0, :, 2])
		confidence = detections[0, 0, i, 2]
        # Only bother with faces over the threshold for true positives
		if confidence > threshold:
			# Start extracting the face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			# It needs some processing
			(startX, startY, endX, endY) = box.astype("int")
			'''if startY - 32 > 0:
				startY -= 32
			if startX - 32 > 0:
				startX -= 32'''
			face = image[startY:endY+32, startX:endX+32]
			(fH, fW) = face.shape[:2]
			if fW < 64 or fH < 64:
				continue
			face = imutils.resize(face, width=HXW, height=HXW)
			# Construct a new filename
			# preprocess.sh renames good filenames, so these new filenames will share same base as original
			filename = os.path.basename(img_path)
			filename, ext = os.path.splitext(filename)
			filename = processed_dir + dataset + "/" + filename + "_" + str(img_itr) + ext
			# If you were renaming here with this script, you would construct this new filename
			#filename = processed_dir + dataset + "/" + str(itr+1) + "_" + str(img_itr) + ".jpg"
			cv2.imwrite(filename, face)
			total_saved += 1
			img_itr += 1
			if one_photo_per_img:
				# Exit for every face detected in the image
				break
		# End if probability for this face is above threshold
	# End for every face detected in the image

	if img_itr == 0:
		# Update this to the list of images that did not extract a face
		double_take.append(img_path)
		# Save a copy of all such files to a separate directory
		# So you can more quickly find and manually process them
		filename = "double_take/" + dataset + "_" + os.path.basename(img_path)
		cv2.imwrite(filename, image)
	# End if there were zero faces extracted from this image
# End looping thru every image in the dataset


print("saved", total_saved, "extracted faces images")

# Update the log of files you need to manually check
# Less important because it's cooler to just save copies of the actual images
if len(double_take) > 0:
	msg = "\n" + str(total_saved) + " faces extracted out of " + str(len(img_paths)) + " images from:\n"
	f.write(msg)
	f.write(originals_dir + dataset)
	f.write("\nZero faces were saved from these images:\n")
	for img_path in double_take:
		f.write(img_path)
		f.write("\n")
f.write("\n")
f.close()



##
