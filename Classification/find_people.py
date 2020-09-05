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

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default=None)
args = vars(ap.parse_args())

img_path = args["image"]

hogCV = cv2.HOGDescriptor()
hogCV.setSVMDetector(
	cv2.HOGDescriptor_getDefaultPeopleDetector()
)

def detect_people(frame):
    boxs, weights = hogCV.detectMultiScale(
        frame, winStride=(4, 4),
        padding=(8, 8), scale=1.04
    )
    ppl = 0
    for x, y, w, h in boxs:
        cv2.rectangle(
            frame, (x,y),
            (x+w, y+h),
            (255, 255, 0), 1
        )
        cv2.putText(
            frame, 'human {}'.format(ppl),
            (x,y), cv2.FONT_HERSHEY_SIMPLEX,
            0.4, (0,255,0), 1
        )
        ppl += 1
    p = "people"
    if ppl == 1:
        p = "person"
    print("Detecting:", ppl, p, "in frame")
    cv2.imshow('output', frame)
    return frame


if img_path is not None:
    img = cv2.imread(img_path)
    img = imutils.resize(img, width=500)
    img = detect_people(img)
    cv2.imshow(img_path, img)
    cv2.waitKey(0)



##
