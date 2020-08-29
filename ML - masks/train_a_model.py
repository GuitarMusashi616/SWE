# Ty Bergstrom
# train_a_model.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Train any model with this file
#
# $ source ./venv1/bin/activate
# $ python3 -W ignore train_a_model.py
#
# This file pre-processes an input dataset with selected parameters
# Trains a selected model with selected parameters and tunings and saves it
# Outputs results and metrics including a plot and saves them with the build info


from sklearn.preprocessing import LabelBinarizer
from processing.process import Pprocess
from processing.results import Result
from processing.tuning import Tune
from nets.net import Quick_Net
from nets.net import Full_Net
import numpy as np
import argparse
import pickle
import time


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--savemodel", type=str, default="processing/model.model")
ap.add_argument("-p", "--plot", type=str, default="processing/plot.png")
ap.add_argument("-d", "--dataset", type=str, default="processed_dataset")
ap.add_argument("-a", "--aug", type=str, default="original")
ap.add_argument("-m", "--model", type=str, default="Quick_Net")
ap.add_argument("-o", "--opt", type=str, default="Adam2")
ap.add_argument("-i", "--imgsz", type=str, default="m")
ap.add_argument("-e", "--num_epochs", type=int, default=50)
ap.add_argument("-b", "--batch_size", type=str, default="m")
ap.add_argument("-k", "--kernelsize", type=int, default=3)
ap.add_argument("-n", "--notes", type=str, default="(none)")
args = vars(ap.parse_args())

num_epochs = args["num_epochs"]
batch_size = Tune.batch_size(args["batch_size"])
HXW = Tune.img_size(args["imgsz"])
kernel = Tune.kernel(args["kernelsize"])
notes = args["notes"]
start_time = time.time()

print("\n...pre-processing the data...\n")
(data, cl_labels) = Pprocess.preprocess(args["dataset"], HXW)
lb = LabelBinarizer()
cl_labels = lb.fit_transform(cl_labels)
num_classes = len(lb.classes_)
loss_type = "binary_crossentropy"
if num_classes > 2:
    loss_type = "categorical_crossentropy"
(train_X, test_X, train_Y, test_Y) = Pprocess.split(data, np.array(cl_labels), num_classes)
aug = Pprocess.data_aug(args["aug"])

print("\n...building the model...\n")
if args["model"] == "Full_Net":
    model = Full_Net.build(width=HXW, height=HXW, depth=3, kernel=kernel, classes=num_classes)
else:
    model = Quick_Net.build(width=HXW, height=HXW, depth=3, kernel=kernel, classes=num_classes)
opt = Tune.optimizer(args["opt"], num_epochs)
model.compile(loss=loss_type, optimizer=opt, metrics=["accuracy"])

print("\n...training the model...\n")
H = model.fit_generator(aug.flow(train_X, train_Y, batch_size=batch_size), validation_data=(test_X, test_Y), 
    steps_per_epoch=len(train_X) // batch_size, epochs=num_epochs, verbose=1)
model.save(args["savemodel"] )
f = open("processing/lb.pickle", "wb")
f.write(pickle.dumps(lb))
f.close()

print("\n...getting results of training & testing...\n")
predictions = model.predict(test_X, batch_size=batch_size)
Result.save_info(start_time, Result.acc_score(test_Y, predictions), args["model"], num_epochs, args["opt"], args["aug"], HXW, batch_size, kernel, len(data), notes)
Result.display_metrix(test_X, test_Y, predictions, model, lb.classes_, aug, batch_size)
Result.display_plot((args["plot"]), num_epochs, H)



##
