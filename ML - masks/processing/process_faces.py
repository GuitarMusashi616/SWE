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
# delete any images that aren't actually a face,
# or later you can manually crop the faces on any that aren't perfect
#
# Other notes:
# This outputs some info to a file named double_take_idx.txt
# It will contain a list of original file paths for any images that did not find a face.
# To help find images that you need to go back and manually process.
# Update:
# Even better I'm just saving copies of those files to processed_dataset/double_take/
# So that you can find and manually process those images much quicker
#
# This is set up to only process one directory at a time, there's a good reason
# Use preprocess.sh to run this on each directory that you need
#
# python3 process_faces.py -d mask
# python3 process_faces.py -d without_mask -o tru


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
ap.add_argument("-o", "--one", type=bool, default=False)
args = vars(ap.parse_args())

# Face detection stuff
proto = "../face_detector/deploy.prototxt"
model = "../face_detector/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(proto, model)
threshold = 0.8 # A probability threshold to decrease false positives

originals_dir = "../original_dataset/"
dataset = args["dataset"]
img_paths = sorted(list(paths.list_images(originals_dir + dataset)))
# Err check that the directory was not empty
if len(img_paths) < 1:
	print("Err: The directory", originals_dir + dataset, "was empty")
	sys.exit(1)

total_saved = 0 # How many total faces were extracted from the dataset
double_take = [] # List of images with zero faces extracted, they will need to be manually processed
f = open("double_take_idx.txt","a+") # Save a log of files that you need to go back & manually process
one_photo_per_img = args["one"] # Save time if you know there is only one face per img in the dataset

print("processing:", len(img_paths), "input images from", originals_dir + dataset)

for (itr, img_path) in enumerate(img_paths):
	name = img_path.split(os.path.sep)[-2]
	image = cv2.imread(img_path)
	(h, w) = image.shape[:2]

	# Detect faces in the image
	imageBlob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 
		1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)
	detector.setInput(imageBlob)
	detections = detector.forward()

	# Counter to check if 0 faces were extracted
	total_saved_per_img = 0

	if len(detections) < 1:
		double_take.append(img_path)
		break
	else:
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
				# Construct a new filename
				# preprocess.sh renames good filenames, so these new filenames will share same base as original
				filename = os.path.basename(img_path)
				filename, ext = os.path.splitext(filename)
				filename = "../processed_dataset/" + dataset + "/" + filename + "_" + str(img_itr) + ext
				# If you were renaming here with this script, you would construct this new filename
				#filename = "../processed_dataset/" + dataset + "/" + str(itr+1) + "_" + str(img_itr) + ".jpg"
				cv2.imwrite(filename, face)
				total_saved += 1
				total_saved_per_img += 1
				img_itr += 1
				if one_photo_per_img:
					# Exit for every face detected in the image
					break
			# End if probability for this face is above threshold
		# End for every face detected in the image
	# End if at least one face detected in this image
	if total_saved_per_img == 0:
		# Update this to the list of images that did not extract a face
		double_take.append(img_path)
		filename = "double_take/" + dataset + "_" + os.path.basename(img_path)
		# Or take it a step further and save copies of all such files to a separate directory
		# So you can more quickly find and manually process them
		cv2.imwrite(filename, image)


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
