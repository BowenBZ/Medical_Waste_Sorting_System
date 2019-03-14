import tensorflow as tf
import numpy as np
import os
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import sys
from time import sleep
import heapq
from operator import itemgetter
import motor_control_all

# The folder that store the models
model_path = './models'
tflite_model_path = os.path.join(model_path, 'model_clean2.tflite')
# Create a tflite interpreter, this is the part of tflite that actually runs models.
interpreter = tf.contrib.lite.Interpreter(model_path=tflite_model_path)
# Allocate memory for the all the weight tensors and such.
interpreter.allocate_tensors()
# Get input and output tensor information.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)
print(output_details)

def run_interpreter(input_data):
    # interpreter.reset_all_variables()
    # Set tensor specifies the input to the model.
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # Invoke is used to run the input through the model.
    interpreter.invoke()
    # We have to use get_tensor to load the output.
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # 
    out = output_data[0]
    #out = np.argmax(output_data)

    return out

class_names = ["background", "pharmaceutical", "sharps", "trace_chemo"]
				
# Set up camera constants
#MAX is 1280
IM_WIDTH = 640
scale = 1 / 2

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
        frame.setflags(write=1)

        height, width, _ = frame.shape
        # resized_frame = frame[:int(height * 2 / 3), int(width / 2) - 213: int(width / 2) + 213, :]
        resized_frame = frame[:int(height * scale), \
                                int(width / 2 - width * scale / 2): int(width / 2 + width * scale / 2), \
                                :]
        resized_frame = cv2.resize(resized_frame, (224, 224))
        resized_frame = (resized_frame / 255).astype(np.float32)

        # resized_frame = cv2.resize(frame, (224, 224))
        # resized_frame = (resized_frame / 255).astype(np.float32)
        if not motor_control_all.is_moving:
            input_data = resized_frame[tf.newaxis, ...]
            predict = run_interpreter(input_data)
            predict_tmp = []
            for num in predict:
                predict_tmp.append(round(num, 4))
            print(predict_tmp)
            if predict_tmp[2] > 0.1:
                predict = 2
            else:
                predict = int(np.argmax(predict))

            print(class_names[predict])
            print('\n')

            if predict != 0:
                motor_control_all.update_state(predict)

        cv2.imshow("window", resized_frame)
        cv2.waitKey(25)

        rawCapture.truncate(0)
except KeyboardInterrupt:
    step_motor.rotate(False)
    camera.close()
    cv2.destroyAllWindows()

