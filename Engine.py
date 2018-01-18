'''
PWM controlled Engine class provides fwd/bwd/stop functionality for IC LH911 
two GPIO/PWM pins are required to control both speed and direction

e1.move(0)
for x in range(100):
    e1.move(x)
    time.sleep(0.1)


e2 = Engine(26,20)
e2.move(30)
e2.move(-30)
'''

import RPi.GPIO as IO
from threading import Thread
import time

class Engine:

    '''
    ctor
    '''    
    def __init__(self, pin1=19, pin2=16):
        IO.setwarnings(False)
        IO.setmode (IO.BCM)
        self.freq=100

        self.pin1 = pin1
        IO.setup(self.pin1,IO.OUT)
        self.pin2 = pin2
        IO.setup(self.pin2,IO.OUT)
        
        self.engineFwd = IO.PWM(self.pin1 , self.freq)
        self.engineFwd.start(0)
        self.engineRwd = IO.PWM(self.pin2 , self.freq)
        self.engineRwd.start(0)

        self.fwd=0
        self.rwd=0

    # TODO: make notification system so that move command is reset after a certain time frame
    def move(self,speed):
        '''
        if speed > 0:
            self.engineRwd.start(0)
            self.engineFwd.start(speed)
        else:
            self.engineRwd.start(abs(speed))
            self.engineFwd.start(0)
        '''
        sign=speed>0
        speed=abs(speed)
        x1 , x2 = sign*speed, int(not(sign))*speed
        self.engineRwd.start(x1)
        self.engineFwd.start(x2)

    def ramp(Engine, value):
        pass

if __name__ == "__main__":

    speed = 80

    #engineLeft = Engine(19,16)
    e1 = Engine(19,16)
    e2 = Engine(20,26)
    # fwd    
    e1.move(speed)
    e2.move(speed)
    time.sleep(0.5)
    e1.move(0)
    e2.move(0)
    time.sleep(1)
    # rwd
    e1.move(-speed)
    e2.move(-speed)
    time.sleep(0.5)
    # quit
    e1.move(0)
    e2.move(0)
    time.sleep(1)
    # turn arround
    e1.move(speed)
    e2.move(-speed)
    time.sleep(1)
    # quit
    e1.move(0)
    e2.move(0)
    time.sleep(1)
    
    


