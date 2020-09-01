# Ty Bergstrom
# net.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Neural network implementations


from keras.layers.convolutional import MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.models import Sequential
from keras.layers.core import Dense
from keras import backend as K


# This is a lightweight net for testing builds and datasets more quickly
class Quick_Net:

	@staticmethod
	def build(width, height, depth, kernel, classes):
		model = Sequential()
		inputShape = (height, width, depth)
		if K.image_data_format() == "channels_first":
			inputShape = (depth, height, width)

		# first set of convolutional relu and pooling layers
		model.add(Conv2D(32, (kernel, kernel), padding="same", input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))

		# second set of convolutional relu and pooling layers
		model.add(Conv2D(64, (kernel, kernel), padding="same"))
		model.add(Activation("relu"))
		model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.1))

		# only set of fully connected relu layers
		model.add(Flatten())
		model.add(Dense(500))
		model.add(Activation("relu"))

		model.add(Dense(classes))
		model.add(Activation("softmax"))

		return model



# This is a deeper bigger net for when you are prepared to wait a while
class Full_Net:

	@staticmethod
	def build(width, height, kernel, depth, classes):
		model = Sequential()
		inputShape = (height, width, depth)
		if K.image_data_format() == "channels_first":
			inputShape = (depth, height, width)

		# first set of convolutional relu and pooling layers
		model.add(Conv2D(32, (kernel, kernel), padding="same", input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))

		# second set of convolutional relu and pooling layers
		model.add(Conv2D(64, (kernel, kernel), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))

		# third set of convolutional relu and pooling layers
		model.add(Conv2D(128, (kernel, kernel), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))

		# fourth set of convolutional relu and pooling layers
		model.add(Conv2D(264, (kernel, kernel), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))

		# only set of fully connected relu layers
		model.add(Flatten())
		model.add(Dense(500))
		model.add(Activation("relu"))

		model.add(Dense(classes))
		model.add(Activation("softmax"))

		return model



##
