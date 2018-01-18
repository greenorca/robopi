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
import Adafruit_PCA9685
from threading import Thread
import time
from Engine import Engine

'''
provides Engine functionality through PCA_9685
'''
class Engine_PCA(Engine):

    '''
    ctor, pin1 and pin2 represent PCA channels
    '''    
    def __init__(self, pin1=0, pin2=1):
        self.freq=100
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.freq)

        self.pin1 = pin1
        self.pin2 = pin2
        self.MAX = 4095
        self.move(0)

    def stop(self):
        self.pwm.set_pwm(self.pin1,0,0)
        self.pwm.set_pwm(self.pin2,0,0)        

    # TODO: make notification system so that move command is reset after a certain time frame
    def move(self,speed):
        if abs(speed)<40:
            self.stop()
            return
        sign=speed>0
        speed=abs(speed)
        x1 = self.MAX - sign*speed/100 * self.MAX
        x2 = self.MAX - int(not(sign))*speed/100 * self.MAX
        print('speed: '+str(x1)+', '+str(x2))
        self.pwm.set_pwm(self.pin1,int(x1),int(self.MAX))
        self.pwm.set_pwm(self.pin2,int(x2),int(self.MAX))


if __name__ == "__main__":

    speed = 80

    #engineLeft = Engine(19,16)
    e1 = Engine_PCA(0,1)
    e2 = Engine_PCA(2,3)
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
    
    


