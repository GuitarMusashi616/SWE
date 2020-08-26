# Ty Bergstrom
# results.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Display metrics and plots for any model
# The classification report and confusion matrix will be output to terminal
# And saved to a file performance.txt along with all of the build parameters
# (Every build is appended to the same file)
# Also save a plot


from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from keras import metrics
import numpy as np
import time
import matplotlib
matplotlib.use("Agg")


class Result:

    # Print the classification report and confusion matrix
	def display_metrix(testX, testY, predictions, model, classes, aug, bs):
		cl = Result.clas_report(testY, predictions, classes)
		cm = Result.confusion(model, aug, testX, testY, predictions)
		print("...classification report\n")
		print(cl)
		print("...confusion matrix\n")
		print(cm)
		print()
		Result.save_results(cl, cm)


	def clas_report(testY, predictions, classes):
		return classification_report(testY.argmax(axis=1), predictions.argmax(axis=1), target_names=classes)


	def confusion(model, aug, testX, testY, predictions):
		predIdxs = model.predict_generator(aug.flow(testX, testY))
		predIdxs = np.argmax(predIdxs, axis=1)
		return confusion_matrix(testY.argmax(axis=1), predictions.argmax(axis=1))


	def display_plot(plot, epochs, H):
		plt.style.use("ggplot")
		plt.figure()
		N = epochs
		plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
		plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
		plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
		plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
		plt.title("Training Loss and Accuracy")
		plt.xlabel("Epoch #")
		plt.ylabel("Loss/Accuracy")
		plt.legend(loc="lower left")
		plt.savefig(plot)
		plt.show()


	# Save the classification report and confusion matrix to file
	def save_results(cl, cm):
		f = open("processing/performance.txt","a+")
		f.write(cl)
		f.write("\n")
		f.write(np.array2string(cm))
		f.write("\n\n\n")
		f.close()


	# Save the build info and parameters to the file
	def save_info(start_time, model, epochs, opt, aug, imgsz, bs, k, datasize, notes):
		run_time = time.time() - start_time
		label = "build: {}, model: {}, epochs: {}, optimzer: {}, augmentation: {}, image size: {}, batch size: {}, kernel size: {}, dataset size: {}, notes: {}, run time: {}\n".format(start_time, model, epochs, opt, aug, imgsz, bs, k, datasize, notes, run_time)
		f = open("processing/performance.txt","a+")
		f.write(label)
		f.write("\n")
		f.close()



##
