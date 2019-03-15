# This script is used to control all the motors including servo motor and step motor with a clean logic

import step_motor_17HS4401A as step_motor
import servo_motor_ld_27mg as servo_motor
import time

is_moving = False

def update_state(state):
	is_moving = True
	step_motor.update_state(state)
	servo_motor.open_close_door()
	step_motor.update_state_reverse(state)
	is_moving = False

if __name__ == "__main__":
	try:
	    while True:
	    	state = int(input("Please input state： "))
	    	update_state(state)
	except KeyboardInterrupt:
	    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")

