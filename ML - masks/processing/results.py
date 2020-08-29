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
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from keras import metrics
import numpy as np
import time
import matplotlib
matplotlib.use("Agg")


class Result:

    # Print the classification report and confusion matrix
	def display_metrix(test_X, test_Y, predictions, model, classes, aug, bs):
		cl = Result.clas_report(test_Y, predictions, classes)
		cm = Result.confusion(model, aug, test_X, test_Y, predictions)
		print("...classification report\n")
		print(cl)
		print("...confusion matrix\n")
		print(cm)
		print()
		Result.save_results(cl, cm)


	def clas_report(test_Y, predictions, classes):
		return classification_report(test_Y.argmax(axis=1), predictions.argmax(axis=1), target_names=classes)


	def confusion(model, aug, test_X, test_Y, predictions):
		predIdxs = model.predict_generator(aug.flow(test_X, test_Y))
		predIdxs = np.argmax(predIdxs, axis=1)
		return confusion_matrix(test_Y.argmax(axis=1), predictions.argmax(axis=1))


	def acc_score(test_Y, predictions):
		return accuracy_score(test_Y.argmax(axis=1), predictions.argmax(axis=1))


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
		plt.legend(loc="center right")
		print("\n", plot, "\n")
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
	def save_info(start_time, acc, model, epochs, opt, aug, imgsz, bs, k, datasize, notes):
		run_time = time.time() - start_time
		label = "build: {} {:.6}%\nmodel: {}, epochs: {}, optimzer: {}, augmentation: {},\nimage size: {}, batch size: {}, kernel size: {}, dataset size: {}, run time: {:.2f}s\nnotes: {} \n".format(start_time, acc*100, model, epochs, opt, aug, imgsz, bs, k, datasize, run_time, notes)
		f = open("processing/performance.txt","a+")
		f.write(label)
		f.write("\n")
		f.close()



##
