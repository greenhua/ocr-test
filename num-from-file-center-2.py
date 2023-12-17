import cv2, os
import numpy as np
import time
import imutils
from processing_2_1 import processing





vid_capture = cv2.VideoCapture('./kr-num4.mov')

vid_capture.set(cv2.CAP_PROP_POS_FRAMES, 80)



i=0

while(vid_capture.isOpened()):
    ret, frame = vid_capture.read()
    i+=1
    if ret == True:
        processing(frame, clahe=False, i=i)



cv2.waitKey(0)
