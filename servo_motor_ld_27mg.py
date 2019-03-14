import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)	# Use pinout to check the pin number
servoPIN = 26
GPIO.setup(servoPIN, GPIO.OUT)

servo_motor = GPIO.PWM(servoPIN, 50)  # Set the frequency to 50Hz, so the duty cycle is 20ms

# motor_moving = False

# The servo motor is controled by the PWM every 20 ms. 
# If the pulse for high is 0.5 ms (duty cycle: 2.5%), the servo angle will be 0;
# If the pulse for high is 2.5 ms (duty cycle: 12.5%), the servo angle will be 270.
def angle_to_duty_cycle(angle):
	pulse_time = 0.5 + angle / 270 * 2
	duty_cycle = pulse_time / 20 * 100
	return duty_cycle

def stop_tmp():
	servo_motor.ChangeDutyCycle(0)

def initialize_motor():
	# Initialization
        servo_motor.start(angle_to_duty_cycle(float(215)))
        time.sleep(1)
	#stop_tmp()

def open_door(flag):
	if flag:
		servo_motor.ChangeDutyCycle(angle_to_duty_cycle(float(170)))
		time.sleep(1)
		#stop_tmp()
	else:
		servo_motor.ChangeDutyCycle(angle_to_duty_cycle(float(230)))
		time.sleep(2)
		#stop_tmp()

if __name__ == "__main__":
	initialize_motor()
	try:
		while True:
			flag = input('Open door(y/n)?: ')
			if flag == 'y':
				open_door(True)
				time.sleep(1)
				open_door(False)
			#angle = input("Please input an angle: ")
			#servo_motor.ChangeDutyCycle(angle_to_duty_cycle(float(angle)))
			#time.sleep(1)
			#stop_tmp()
	except KeyboardInterrupt:
		#servo_motor.ChangeDutyCycle(angle_to_duty_cycle(float(90)))
		#time.sleep(1)
		servo_motor.stop()
		GPIO.cleanup()
