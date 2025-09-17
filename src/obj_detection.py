import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cascade = cv.CascadeClassifier('stop_data.xml')
    found = cascade.detectMultiScale(frame, minSize=(20, 20))
    for (x, y, w, h) in found:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

    cv.imshow('MED-ID', frame)
    if cv.waitKey(1) == ord('q'):
        break







# When everything done, release the capture
cap.release()
cv.destroyAllWindows()