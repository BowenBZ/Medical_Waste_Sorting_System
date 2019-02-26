import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
control_pins1 = [2,3,4,17]
control_pins2 = [14,15,18,23]
control_pins3 = [6,13,19,26]

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

def angle2step(angle):
  return int(angle / 90.0 * 150.0)

class step_motor:
  def __init__(self, control_pins):
    self.control_pins = control_pins
    for pin in control_pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, 0)

  def go_forward(self, steps):
    for i in range(steps):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(self.control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
    self.stop()

  def go_backward(self, steps):
    for i in range(steps):
      for halfstep in reversed(range(8)):
        for pin in range(4):
          GPIO.output(self.control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
    self.stop()

  def stop(self):
    for pin in range(4):
      GPIO.output(self.control_pins[pin], 0)


def door_motion():
  # open door
  left_door.go_forward(angle2step(50))
  right_door.go_backward(angle2step(50))

  # wait time
  time.sleep(1)

  # close door
  left_door.go_backward(angle2step(50))
  right_door.go_forward(angle2step(50))

# 308 is a circle, 77 is a kind, go_forward is clock direction
motor_moving = False
state = 1
def classify(target):
  # Set global
  global state
  # Update the condition
  motor_moving = True
  # Check wether is the over
  if not target:
    is_stop = 1
    target = 1
  else:
    is_stop = 0
  # Move the classify
  if target != state:
    direction = target - state
    state = target
    if direction == 1 or direction == -3:
      classify_motor.go_backward(angle2step(77))
    elif direction == 2 or direction == -2:
      classify_motor.go_forward(angle2step(77 * 2))
    else:
      classify_motor.go_forward(angle2step(77))
  # Move the door
  if not is_stop:
    door_motion()
  # Wait a little time
  time.sleep(1)
  # Update the condition
  motor_moving = False

# 1 
# 2(1): ni 1
# 3(2): ni/sh 2
# 4(3): sh 1

# 2
# 1(-1): sh 1
# 3(1): ni 1
# 4(2): sh/ni 2

# 3
# 1(-2): sh/ni 2
# 2(-1): sh 1
# 4(1): ni 1

# 4
# 1(-3): ni 1
# 2(-2): ni/sh 2
# 3(-1): sh 1


left_door = step_motor(control_pins1)
right_door = step_motor(control_pins2)
classify_motor = step_motor(control_pins3)

if __name__ == "__main__":
  try:
    while True:
      pass
      # direction = input("Go forward?(y/n): ")
      # angle = input("Please input the angle: ")
      # if direction == 'y':
      #   left_door.go_forward(angle2step(int(angle)))
      # else:
      #   left_door.go_backward(angle2step(int(angle)))


      # ifopen = input("Open?(y/n): ")
      # if ifopen == 'y':
      #   open_door(True)
      # else:
      #   open_door(False)

      category = input("Please input category: ")
      classify(int(category))

  except KeyboardInterrupt:
    classify(0)
    GPIO.cleanup()
