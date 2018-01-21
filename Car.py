#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Engine_PCA import Engine_PCA
from OledDisplay import OledDisplay
from UltraSonicDistance import UltraSonicDistanceSensor
from PCA_9685_Stepper import Stepper_PCA9685
from threading import Timer
import os
import configparser
'''
car contains leftWheel and rightWheel, both instances of PWM controlled Engine client_address
both wheels will be stopped 1 second after a moveCar command was issued
'''
class Car:
    leftWheel = None
    rightWheel = None
    display = None
    maxSpeed = 100

    head = None

    leftSpeed = 0;
    rightSpeed = 0;

    # emergency brake: timed thread that automatically stops car after a while
    __timeout = 0.4
    __eBrake = None
    __distanceInterval = 0.1
    __eDist = None

    def __init__(self):
        try:
            config = configparser.ConfigParser()
            mypath = os.path.dirname(os.path.realpath(__file__))+'/robopi_PCA.conf'
            print('debug Car(): '+ mypath)
            config.read(mypath)
            self.leftWheel = Engine_PCA(int(config['robopi']['left_wheel_fwd']),int(config['robopi']['left_wheel_rwd']))
            self.rightWheel = Engine_PCA(int(config['robopi']['right_wheel_fwd']),int(config['robopi']['right_wheel_rwd']))
            self.__ebrake = Timer(self.__timeout, self.stop)

            self.distance_front_left = UltraSonicDistanceSensor(
                int(config['robopi']['usd__front_left_trigger']),
                int(config['robopi']['usd__front_left_echo']))

            self.distance_front_right = UltraSonicDistanceSensor(
                int(config['robopi']['usd__front_right_trigger']),
                int(config['robopi']['usd__front_right_echo']))

            self.head = Stepper_PCA9685(freq = 1000, MAX = 4095, channel=[4,5,6,7])
            

        except Exception as e:
            raise e


    def __observeDistance(self):
        if self.leftSpeed == 0 and self.rightSpeed == 0:
            return

        if self.distance_front_right.getDistance() < 15 and self.leftSpeed > 0  or self.distance_front_left.getDistance() < 15 and self.rightSpeed > 0:
            print("limit reached...")
            self.stop()
            return;

        self.__eDist = Timer(self.__distanceInterval,self.__observeDistance)
        self.__eDist.start()

    def moveHead(self, steps=10):
        if steps > 0:
            self.head.stepClockwise(min(steps,200))
        else:
            self.head.stepCounterClockwise(min(abs(steps),200))
        


    def moveCar(self, leftSpeed=0, rightSpeed=0):
        try:
            self.__eBrake.cancel()
            self.__eDist.cancel()
        except:
            pass
        
        self.leftWheel.move(leftSpeed)
        self.rightWheel.move(rightSpeed)

        self.leftSpeed = leftSpeed
        self.rightSpeed = rightSpeed

        self.__eDist = Timer(self.__distanceInterval,self.__observeDistance)
        self.__eDist.start()

        #setup timer 
        self.__eBrake = Timer(self.__timeout,self.stop)
        self.__eBrake.start()

    def stop(self):
        print("reseting wheel speed")
        self.leftWheel.move(0)
        self.rightWheel.move(0)
        self.leftSpeed = 0
        self.rightSpeed = 0
        try:
            self.__eBrake.cancel()
            self.__eDist.cancel()
        except:
            pass


if __name__=="__main__":
    car = Car()