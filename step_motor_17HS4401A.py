from time import sleep
import pigpio

DIR = 20
STEP = 21
SLEEP = 2

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)
pi.set_mode(SLEEP, pigpio.OUTPUT)

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins

RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
for i in range(3):
    pi.write(MODE[i], RESOLUTION['1/32'][i])

pi.write(DIR, 1)  # Set direction

def rotate(flag):
	if flag:
		pi.write(SLEEP, 1)
		# Set duty cycle and frequency
		pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Off
		pi.set_PWM_frequency(STEP, 500)  # 500 pulses per second
	else:
		pi.write(STEP, 0) 
		sleep(2)
		pi.write(SLEEP, 0)
		# sleep(2)
		# pi.write(SLEEP, 0)

def run(time):
	rotate(True)
	sleep(time)
	rotate(False)

delta_time = 1.6

def update_state(new_state):
	if new_state == 1:
		pi.write(DIR, 1)
		run(delta_time)
	elif new_state == 2:
		pi.write(DIR, 0)
		run(delta_time)
	elif new_state == 3:
		pi.write(DIR, 0)
		run(delta_time * 3)

def update_state_reverse(pre_state):
	if pre_state == 1:
		pi.write(DIR, 0)
		run(delta_time)
	elif pre_state == 2:
		pi.write(DIR, 1)
		run(delta_time)
	elif pre_state == 3:
		pi.write(DIR, 1)
		run(delta_time * 3)

if __name__ == "__main__":
	try:
	    while True:
	    	time = input("Please input the seconds you want to run： ")
	    	if float(time) > 0:
	    		pi.write(DIR, 1)  # Set direction
	    	else:
	    		pi.write(DIR, 0)
	    	rotate(True)
	    	sleep(abs(float(time)))
	    	rotate(False)
	except KeyboardInterrupt:
	    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
	finally:
		rotate(False)
		pi.write(SLEEP, 0)
		pi.write(STEP, 0)
		pi.write(DIR, 0)
		pi.stop()
