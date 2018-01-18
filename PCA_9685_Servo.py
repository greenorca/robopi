#!/usr/bin/python3
# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 120  # Min pulse length out of 4096
servo_max = 590  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 50       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)
channel = 15

print('Moving servo, press Ctrl-C to quit...')
pos = servo_min
while True:
    time.sleep(0.8)
    while pos < servo_max:
        pos += 100
        # Move servo on channel O between extremes.
        pwm.set_pwm(channel, 0, pos)
        time.sleep(0.8)

    pos=servo_max
    pwm.set_pwm(15,0,pos)
    
    while pos > servo_min:
        pos -= 100
        # Move servo on channel O between extremes.
        pwm.set_pwm(channel, 0, pos)
        time.sleep(0.8)
    
    pos=servo_min
    pwm.set_pwm(15,0,pos)
