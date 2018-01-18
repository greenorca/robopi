#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from Engine_PCA import Engine_PCA
from OledDisplay import OledDisplay
from UltraSonicDistance import UltraSonicDistanceSensor
from threading import Timer
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

    

    # emergency brake: timed thread that automatically stops car after a while
    __timeout = 1
    __eBrake = None


    def __init__(self):
        try:
            config = configparser.ConfigParser()
            config.read('robopi_PCA.conf')
            self.leftWheel = Engine_PCA(int(config['robopi']['left_wheel_fwd']),int(config['robopi']['left_wheel_rwd']))
            self.rightWheel = Engine_PCA(int(config['robopi']['right_wheel_fwd']),int(config['robopi']['right_wheel_rwd']))
            self.__ebrake = Timer(self.__timeout, self.stop)

            self.distance_front_left = UltraSonicDistanceSensor(int(config['robopi']['usd__front_left_trigger']),
                int(config['robopi']['usd__front_left_echo']))

            self.distance_front_right = UltraSonicDistanceSensor(int(config['robopi']['usd__front_right_trigger']),
                int(config['robopi']['usd__front_right_echo']))

        except Exception as e:
            raise e




    def moveCar(self, leftSpeed=0, rightSpeed=0):
        try:
            self.__eBrake.cancel()
        except:
            pass
        
        self.leftWheel.move(leftSpeed)
        self.rightWheel.move(rightSpeed)

        self.__eBrake = Timer(self.__timeout,self.stop)
        self.__eBrake.start()

    def stop(self):
        print("reseting wheel speed")
        self.leftWheel.move(0)
        self.rightWheel.move(0)
