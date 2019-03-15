# This script is used to check the settings of the camera

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

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize Picamera and grab reference to the raw capture
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_WIDTH)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_WIDTH))
rawCapture.truncate(0)

try:
    for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame1.array
        height, width, _ = frame.shape
        frame = frame[:int(height * 2 / 3), int(width / 2) - 213: int(width / 2) + 213, :]
        # frame.setflags(write=1)
        cv2.imshow('Object detector', frame)
        cv2.waitKey(1)
        rawCapture.truncate(0)
except KeyboardInterrupt:
    camera.close()
    cv2.destroyAllWindows()

