# Ty Bergstrom
# remove_duplicates.py
# CSCE A401
# August 2020
# Software Engineering Project

# Input a dataset and find duplicates
# Generate hashes for each image to find duplcate hashes
# Important for ML projects because duplicates can cause bias
#
# python3 remove_duplicates.py -d ../original_dataset/mask
# python3 remove_duplicates.py -d ../original_dataset/without_mask
#
# optional arg -s to display the duplicates for assurance
# optional arg -r to actually remove duplicates for safety
#
# This is only set up to process one directory at a time
# Use preprocess.sh to easily run it on all the directories you need
#
# Note: I made it so that while the duplicates are being displayed,
# you have like 3 seconds to press the "s" key to pass deleting it


from imutils import paths
import numpy as np
import argparse
import cv2
import os


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True)
ap.add_argument("-r", "--remove", type=bool, default=False)
ap.add_argument("-s", "--show", type=bool, default=False)
args = vars(ap.parse_args())
hash_size = 8

img_paths = list(paths.list_images(args["dataset"]))
# Err check that the directory was not empty
if len(img_paths) < 1:
	print("Err: The directory", args["dataset"] + len(img_paths) , "was empty")
	sys.exit(1)
hashes = {} # dictionary of hashes of the images
total_duplicates = 0

# Part one, loop through the input images and generate their hashes
print("Generating hashes...")
for img_path in img_paths:
	print(img_path)
	img = cv2.imread(img_path)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (hash_size + 1, hash_size))
	# compute a horizontal gradient between adjacent column pixels
	diff = img[:, 1:] > img[:, :-1]
	# convert the difference image to a hash
	img_hash = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
	# find any other image paths with the same hash and add the current image
	paths = hashes.get(img_hash, [])
	# and store the list of paths back in the hashes dictionary
	paths.append(img_path)
	hashes[img_hash] = paths

# Part two, loop through the hashes and find duplicates
print("Finding duplicates...")
for (img_hash, hashed_paths) in hashes.items():
	# Is there more than one image with the same hash
	if len(hashed_paths) > 1:
		# Display the duplicates
		if args["show"]:
			montage = None
			for path in hashed_paths:
				image = cv2.imread(path)
				image = cv2.resize(image, (150, 150))
				if montage is None:
					montage = image
				else:
					montage = np.hstack([montage, image])
			cv2.imshow("Duplicates", montage)
			# You have waitKay(1200) much time to press "s" key to pass deleting ;)
			if cv2.waitKey(1200) == ord("s"):
				print("Duplicate image" + path + "was NOT deleted")
				continue
		# Remove the duplicates
		if args["remove"]:
			for path in hashed_paths[1:]:
				os.remove(path)
				total_duplicates += 1
				print("Duplicate image" + path + "was deleted")

print(total_duplicates, "duplicates were removed")



##
