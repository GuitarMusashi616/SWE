# Ty Bergstrom
# process.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Pre-process the dataset for any model


from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import numpy as np
import random
import cv2
import os


class Pprocess:

	# load the input dataset and process
	def preprocess(dataset, HXW):
		data = []
		cl_labels = []
		img_paths = sorted(list(paths.list_images(dataset)))
		random.seed(64)
		random.shuffle(img_paths)
		for img_path in img_paths:
			img = cv2.imread(img_path)
			img = cv2.resize(img, (HXW, HXW))
			img = img_to_array(img)
			data.append(img)
			label = img_path.split(os.path.sep)[-2]
			cl_labels.append(label)
		data = np.array(data, dtype="float") / 255.0
		return data, cl_labels


	# Using sklearn train test split, but with additional required processing for binary classification
	def split(data, cl_labels, num_classes):
		(train_X, test_X, train_Y, test_Y) = train_test_split(data, cl_labels, test_size=0.2, random_state=64)
		if num_classes == 2:
			train_Y = to_categorical(train_Y, num_classes=num_classes)
			test_Y = to_categorical(test_Y, num_classes=num_classes)
		return train_X, test_X, train_Y, test_Y


	# different options for augmentation pre-processing
	def data_aug(aug):
		if aug == "original":
			return ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
            height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
			horizontal_flip=True, fill_mode="nearest")
		elif aug == "light1":
			return ImageDataGenerator(rotation_range=15, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.1, zoom_range=0.1,
			horizontal_flip=True, fill_mode="nearest")
		elif aug == "light2":
			return ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.1, zoom_range=0.1,
			horizontal_flip=True, fill_mode="reflect")
		elif aug == "light3":
			return ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
			horizontal_flip=True, fill_mode="wrap")
		elif aug == "medium1":
			return ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
			brightness_range=[1.0,1.5],	horizontal_flip=True, fill_mode="nearest")
		elif aug == "medium2":
			return ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
			brightness_range=[0.5,1.0],	horizontal_flip=True, fill_mode="nearest")
		elif aug == "medium3":
			return ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.2, zoom_range=0.2, horizontal_flip=True,
			vertical_flip=True, fill_mode="nearest")
		elif aug == "heavy1":
			return ImageDataGenerator(rotation_range=45, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.2, zoom_range=1.2,
			brightness_range=[1.0,1.0],	horizontal_flip=True, fill_mode="nearest")
		elif aug == "heavy2":
			return ImageDataGenerator(rotation_range=45, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.2, zoom_range=1.2,
			brightness_range=[0.5,1.0],	horizontal_flip=True, fill_mode="nearest")
		else:
			return ImageDataGenerator(rotation_range=15, width_shift_range=0.1,
			height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
			horizontal_flip=True, fill_mode="nearest")



##
