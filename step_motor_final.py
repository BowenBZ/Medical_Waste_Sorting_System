from time import sleep
import RPi.GPIO as GPIO
import time

DIR = 20
STEP = 21
SLEEP = 2

GPIO.setmode(GPIO.BCM)	# Use pinout to check the pin number
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(SLEEP, GPIO.OUT)

step_motor = GPIO.PWM(STEP, 500)
step_motor.ChangeDutyCycle(50)

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins

RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
for i in range(3):
	GPIO.setup(MODE[i], GPIO.OUT)
	GPIO.output(MODE[i], RESOLUTION['1/32'][i])

GPIO.output(DIR, 1)  # Set direction

def rotate(flag):
	if flag:
		GPIO.output(SLEEP, 1)
	else:
		GPIO.output(SLEEP, 0) 

def rotate_angle(angle):
	run_time = angle / 360 * 1.6 # 1.6s is 360
	rotate(True)
	sleep(run_time)
	rotate(False)

if __name__ == "__main__":
	try:
	    while True:
	    	time = input("Please input the seconds you want to run： ")
	    	if float(time) > 0:
	    		GPIO.output(DIR, 1)  # Set direction
	    	else:
	    		GPIO.output(DIR, 0)
	    	rotate(True)
	    	sleep(abs(float(time)))
	    	rotate(False)
	except KeyboardInterrupt:
	    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
	finally:
		rotate(False)
		GPIO.output(SLEEP, 0)
		GPIO.output(STEP, 0)
		GPIO.output(DIR, 0)
		GPIO.cleanup()
