# Ty Bergstrom
# process_faces.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Trying out the OpenCV people detector
# Testing with images, it's easy to set up for video
# Doesn't seem like it's best for this project
# It's trivial for detecting people in video,
# But not good for extracting faces at the same time
#
# $ python3 find_people.py -i img.jpg


import cv2
import imutils
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
args = vars(ap.parse_args())

img_path = args["image"]

# One implementation

hogCV = cv2.HOGDescriptor()
hogCV.setSVMDetector(
	cv2.HOGDescriptor_getDefaultPeopleDetector()
)

def detect_humans(frame):
    boxs, weights = hogCV.detectMultiScale(
        frame, winStride=(4, 4),
        padding=(8, 8), scale=1.04
    )
    ppl = 0
    for x, y, w, h in boxs:
        cv2.rectangle(
            frame, (x, y),
            (x + w, y + h),
            (255, 255, 0), 1
        )
        cv2.putText(
            frame, 'human {}'.format(ppl),
            (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.4, (0, 255, 0), 1
        )
        ppl += 1
    return frame, ppl


# Another implementation, not as good

cascadeCF = cv2.CascadeClassifier(
    "haarcascade/haarcascade_fullbody.xml"
    #cv2.data.haarcascades + "haarcascade_fullbody.xml"
)

def detect_people(frame):
    gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    boxs = cascadeCF.detectMultiScale(gframe, 1.3, 5)
    for x, y, w, h in boxs:
	    cv2.rectangle(
            frame, (x, y),
            (x + w, y + h),
            (255, 0, 255), 2
        )
    ppl = boxs.shape[0]
    print(ppl, "detections")
    return frame, ppl


# Other implementation, not as good

net = cv2.dnn.readNetFromCaffe(
    "mobilenet_ssd/MobileNetSSD_deploy.prototxt",
    "mobilenet_ssd/MobileNetSSD_deploy.caffemodel"
)

def find_peoples(frame):
    frame = imutils.resize(frame, width=500)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    blob = cv2.dnn.blobFromImage(frame, 0.007843, frame.shape[:2], 127.5)
    net.setInput(blob)
    detections = net.forward()
    ppl = 0
    for i in np.arange(0, detections.shape[2]):
        if detections[0, 0, i, 2] < 0.75:
            continue
        if int(detections[0, 0, i, 1]) != 15:
            continue
        (h, w) = frame.shape[:2]
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (start_x, start_y, endX, endY) = box.astype("int")
        person = frame[start_y:endY+32, start_x:endX+32]
        cv2.rectangle(
            frame, (start_x, start_y),
            (endX, endY), (255, 0, 255), 2
        )
        ppl += 1
    return frame, ppl


def displ(frame, ppl):
    p = "people"
    if ppl == 1:
        p = "person"
    print("Detected:", ppl, p, "in frame")
    cv2.imshow(img_path, frame)
    cv2.waitKey(0)


if img_path is not None:
    img = imutils.resize(
        cv2.imread(img_path),
        width=500
    )
    #frame, ppl = detect_humans(img)
    #frame, ppl = detect_people(img)
    frame, ppl = find_peoples(img)
    displ(frame, ppl)


##
