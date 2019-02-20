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

def get_file_num(DIR):
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# The folder that store the images
data_path = './dataset'
# Get the categories that the image belongs to
category = input('Please input the category of the item that you are collecting:\n')
# Record the index of the images
image_index = 0
if os.path.isdir(data_path + '/' + category):
    image_index = get_file_num(data_path + '/' + category)
else:
    os.mkdir(data_path + '/' + category)

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

# Wait the camera set up
wait_time = 4
current_time = 0

try:
    for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # t1 = cv2.getTickCount()
        
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = frame1.array
        frame.setflags(write=1)
        # frame_expanded = np.expand_dims(frame, axis=0)

        #cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        if current_time > wait_time:
            cv2.imshow('Object detector', frame)
            print(frame.shape, image_index)
            filename = data_path + '/' + category + '/' + \
                        category + '_' + str(image_index) +'.jpg'
            cv2.imwrite(filename, frame)
            image_index += 1

        current_time += 1

        # t2 = cv2.getTickCount()
        # time1 = (t2-t1)/freq
        # frame_rate_calc = 1/time1

        # Press 'q' to quit
        sleep(1.5)
        rawCapture.truncate(0)
except KeyboardInterrupt:
    camera.close()
    cv2.destroyAllWindows()

