print("testThermocouple")

import time
import bitbangio
import board
# from adafruit_motorkit import MotorKit
# from adafruit_motor import stepper

i2c = bitbangio.I2C(board.SCL, board.SDA)
