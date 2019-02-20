# Author: Bowen Zhang
#xvfb-run python3 data_collection.py

# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import sys
#import serial
#from pyfirmata import Arduino, util
from time import sleep

# Set up camera constants
#MAX is 1280
IM_WIDTH = 640
IM_HEIGHT = 640

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize Picamera and grab reference to the raw capture
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

try:
    for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame1.array
        # frame.setflags(write=1)
        cv2.imshow('Object detector', frame)
        cv2.waitKey(1)
        rawCapture.truncate(0)
except KeyboardInterrupt:
    camera.close()
    cv2.destroyAllWindows()

