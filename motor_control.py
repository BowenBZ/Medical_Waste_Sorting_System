import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)	# Use pinout to check the pin number
servoPINs = [17, 27, 22]
for servoPIN in servoPINs:
	GPIO.setup(servoPIN, GPIO.OUT)

# Define the motors
# The initial angle of left motor is 0, the turning angle is 40
# The initial angle of right motor is 170, the turning angle is 40
# The initial angle of classify is 0, the turning angle is 58
motor_left = GPIO.PWM(servoPINs[0], 50)
motor_right = GPIO.PWM(servoPINs[1], 50)
motor_classify = GPIO.PWM(servoPINs[2], 50)

left_door_initial_angle = 0
right_door_initial_angle = 165
left_door_delta = 50
right_door_delta = -50
classify_delta = 58

motor_moving = False

# The servo motor is controled by the PWM every 20 ms. 
# If the pulse for high is 0.5 ms (duty cycle: 2.5%), the servo angle will be 0;
# If the pulse for high is 1.5 ms (duty cycle: 7.5%), the servo angle will be 90;
# If the pulse for high is 2.5 ms (duty cycle: 12.5%), the servo will be 180.
def angle_to_duty_cycle(angle):
	pulse_time = 0.5 + angle / 180 * 2
	duty_cycle = pulse_time / 20 * 100
	return duty_cycle

def stop_tmp_all():
	stop_tmp(motor_left)
	stop_tmp(motor_right)
	stop_tmp(motor_classify)

def stop_tmp(motor):
	motor.ChangeDutyCycle(0)

def handle_classify(category):
	motor_moving = True
	motor_classify.ChangeDutyCycle(angle_to_duty_cycle((category - 1) * classify_delta))
	time.sleep(1)
	motor_left.ChangeDutyCycle(angle_to_duty_cycle(left_door_initial_angle + left_door_delta))
	motor_right.ChangeDutyCycle(angle_to_duty_cycle(right_door_initial_angle + right_door_delta))
	# Wait all the motor finish their movements
	time.sleep(1)
	# Avoid shake
	stop_tmp_all()
	# Wait the trash go down
	time.sleep(1)

	motor_left.ChangeDutyCycle(angle_to_duty_cycle(left_door_initial_angle))
	motor_right.ChangeDutyCycle(angle_to_duty_cycle(right_door_initial_angle))
	time.sleep(1)
	stop_tmp_all()
	motor_moving = False

def initialize_motor():
	# Initialization
	motor_left.start(angle_to_duty_cycle(left_door_initial_angle)) 
	motor_right.start(angle_to_duty_cycle(right_door_initial_angle))
	motor_classify.start(angle_to_duty_cycle(0))
	time.sleep(1)
	stop_tmp_all()


if __name__ == "__main__":
	initialize_motor()
	try:
		while True:
			category = input("Please input a category (1-3): ")
			handle_classify(int(category))
	except KeyboardInterrupt:
		motor_leftdoor.stop()
		motor_rightdoor.stop()
		motro_classify.stop()
		GPIO.cleanup()