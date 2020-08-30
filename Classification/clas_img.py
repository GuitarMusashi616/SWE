# Ty Bergstrom
# clas_img.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Loop through one or more input images
# For each detected face in the image
# Extract the face and show it to the model
# Make a prediction
# Draw the bounding box around the face with the prediction label
# Also some debugging output
# Mostly prep for applying this classification to video stream
#
# $ source ./venv1/bin/activate
# $ python3 -W ignore clas_img.py -d img_inputs/tests


from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils import paths
import face_recognition
import numpy as np
import argparse
import imutils
import pickle
import cv2
import sys
import os

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", default="../ML - masks/processing/model.model")
ap.add_argument("-l", "--labelbin", default="../ML - masks/processing/lb.pickle")
ap.add_argument("-s", "--size", type=int, default="48")
ap.add_argument("-i", "--image", required=False)
ap.add_argument("-d", "--dir", required=False)
args = vars(ap.parse_args())

if not args["image"] and not args["dir"]:
	sys.exit(1)
if args["dir"]:
    dataset = args["dir"]
if args["image"]:
    dataset = args["image"]
detection = "hog"
detection = "cnn"
proto = "../ML - masks/face_detector/deploy.prototxt"
model = "../ML - masks/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(proto, model)
threshold = 0.7
HXW = (args["size"])
model = load_model(args["model"])
lb = pickle.loads(open(args["labelbin"], "rb").read())
img_paths = sorted(list(paths.list_images(dataset)))

dbug_imshow = False
clas_imshow = False
dbug_print = True
dbug_total_faces = 0
dbug_total_faces_fr = 0

for img_path in img_paths:
    img = cv2.imread(img_path)
    img = imutils.resize(img, width=500)
    (h, w) = img.shape[:2]

    img_path = os.path.splitext(os.path.basename(img_path))[0]
    if dbug_print:
        print("Processing:", img_path)

    # Detect faces in the image
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)
    detector.setInput(blob)
    detections = detector.forward()

    # For every face detected in the image
    for i in range(0, detections.shape[2]):
        probability = detections[0, 0, i, 2]
        if probability > threshold:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, endX, endY) = box.astype("int")
            # FYI this is a necessary resize so that cv2.resize() doesn't fail
            if start_y - 32 > 0:
                start_y -= 32
            if start_x - 32 > 0:
                start_x -= 32
            # Extract the face image from the original image
            face = img[start_y:endY+32, start_x:endX+32]
            (fH, fW) = face.shape[:2]
            if fW < 64 or fH < 64:
                print("continue, too small")
                continue
            if dbug_imshow:
                face_dbug = imutils.resize(face, width=256, height=256)
                cv2.imshow("Face: {:.2f}%".format(probability), face_dbug)
                cv2.waitKey(400)
            # Resize to the size that the model was trained with
            face = cv2.resize(face, (HXW, HXW))
            # Pre-processing the face to the format that the model requires
            face = face.astype("float") / 255.0
            face = img_to_array(face)
            face = np.expand_dims(face, axis=0)
            # Make the prediction
            prob = model.predict(face)[0]
            idx = np.argmax(prob)
            prediction = lb.classes_[idx]
            # Format output and draw on the original image
            color = (0, 0, 0)
            if prediction == lb.classes_[0]:
                color = (255, 255, 0)
            else:
                color = (0, 0, 255)
            label = "{}: {:.2f}%".format(prediction, prob[idx] * 100)
            loc = start_y - 10 if start_y - 10 > 10 else start_y + 10
            cv2.rectangle(img, (start_x, start_y), (endX, endY), color, 2)
            cv2.putText(img, label, (start_x, loc), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            if dbug_print:
                print("  Detected face: {:.2f}%".format(probability * 100))
                print("    ", label)
                dbug_total_faces += 1

    if clas_imshow:
        cv2.imshow(img_path, img)
        cv2.waitKey(500)

    '''rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model=detection)
    for (top, right, bottom, left) in boxes:
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        #cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        dbug_total_faces_fr += 1
    cv2.imshow(img_path, img)
    cv2.waitKey(500)'''




if dbug_print:
    print("dbug_total_faces:", dbug_total_faces)
    print("dbug_total_faces_fr:", dbug_total_faces_fr)



    ##