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

frame = cv2.imread('/home/pi/Ecomed/dataset/sharps/sharps_4585.jpg')

height, width, _ = frame.shape
# resized_frame = frame[:int(height * 2 / 3), int(width / 2) - 213: int(width / 2) + 213, :]
resized_frame = frame[:int(height * scale), \
                        int(width / 2 - width * scale / 2): int(width / 2 + width * scale / 2), \
                        :]
resized_frame = cv2.resize(resized_frame, (224, 224))
resized_frame = (resized_frame / 255).astype(np.float32)

for i in range(10):
    predict = run_interpreter(resized_frame[tf.newaxis, ...])
    print(predict)
