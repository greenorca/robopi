#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Engine_PCA import Engine_PCA
from OledDisplay import OledDisplay
from UltraSonicDistance import UltraSonicDistanceSensor
from PCA_9685_Stepper import Stepper_PCA9685
import threading, time
from threading import Timer
from queue import Queue
import os, re
import configparser
'''
car contains leftWheel and rightWheel, both instances of PWM controlled Engine client_address
both wheels will be stopped 1 second after a moveCar command was issued
'''
class Car(threading.Thread):

    leftWheel = None
    rightWheel = None
    display = None
    maxSpeed = 100

    distance_FL = 0
    distance_FR = 0
    dist_err = 10

    head = None

    leftSpeed = 0
    rightSpeed = 0

    # emergency brake: timed thread that automatically stops car after a while
    __timeout = 0.4
    __eBrake = None
    __distanceInterval = 0.1
    __eDist = None

    # expect messages like 'l65;r63;' 'l-345;r-23;'
    wheel_pattern = re.compile(r"L(-*\d+);R(-*\d+);")
    #first decimal for clockwise/counterclockwise turns, second decimal for head up/down
    head_pattern = re.compile(r"H:(-*\d+);(-*\d+);")


    def run(self):
        data=""
        while (data!="xxx"):
            if (not(self.queue.empty())):
                data = self.queue.get()
                match = re.match(self.wheel_pattern, data) #here's for the wheels
                if match:
                    leftSpeed = int(match.group(1))
                    rightSpeed = int(match.group(2))
                    self.moveCar(leftSpeed, rightSpeed)
                    print('Moving: '+str(leftSpeed)+', '+str(rightSpeed))
                    #self.display.setLine3("L:"+str(leftSpeed)+" R:"+str(rightSpeed))
                else:
                    match = re.match(self.head_pattern, data)
                    if match:
                        headTurns = int(match.group(1))
                        headUpDown = int(match.group(2))
                        self.moveHead(headTurns)
                        print('Moving head: '+str(headTurns)+', Up/Down:'+str(headUpDown))
                        #self.display.setLine3("L:"+str(leftSpeed)+" R:"+str(rightSpeed))
                    else:
                        print('Pattern mismatch')
                        #self.display.setLine3("Pattern mismatch")

            time.sleep(0.1)


    def __init__(self, queue):
        super(Car,self).__init__()
        try:
            self.queue = queue
            config = configparser.ConfigParser()
            mypath = os.path.dirname(os.path.realpath(__file__))+'/robopi_PCA.conf'
            print('debug Car(): '+ mypath)
            config.read(mypath)
            self.leftWheel = Engine_PCA(int(config['robopi']['left_wheel_fwd']),int(config['robopi']['left_wheel_rwd']))
            self.rightWheel = Engine_PCA(int(config['robopi']['right_wheel_fwd']),int(config['robopi']['right_wheel_rwd']))
            self.__ebrake = Timer(self.__timeout, self.stop)

            self.distance_sensor_front_left = UltraSonicDistanceSensor(
                int(config['robopi']['usd__front_left_trigger']),
                int(config['robopi']['usd__front_left_echo']))

            self.distance_sensor_front_right = UltraSonicDistanceSensor(
                int(config['robopi']['usd__front_right_trigger']),
                int(config['robopi']['usd__front_right_echo']))

            self.distance_FR = self.distance_sensor_front_right.getDistance()
            self.distance_FL = self.distance_sensor_front_left.getDistance()

            self.head = Stepper_PCA9685(freq = 1000, MAX = 4095, channel=[4,5,6,7])


        except Exception as e:
            raise e


    '''
    keep track of current distances (front left and right)
    stop engine of distance too short
    '''
    def __observeDistance(self):

        if self.leftSpeed == 0 and self.rightSpeed == 0:
            return

        self.distance_FR = self.distance_sensor_front_right.getDistance()
        self.distance_FL = self.distance_sensor_front_left.getDistance()

        if self.distance_FR < self.dist_err and self.leftSpeed > 0  or self.distance_FL < self.dist_err and self.rightSpeed > 0:
            print("limit reached...")
            self.stop()
            return;

        self.__eDist = Timer(self.__distanceInterval,self.__observeDistance)
        self.__eDist.start()

    '''
    moves "head", use positive values to turn clockwise, negative values to turn counterclockwise

    '''
    def moveHead(self, steps=10):
        if steps > 0:
            self.head.stepClockwise(min(steps,200))
        else:
            self.head.stepCounterClockwise(min(abs(steps),200))


    '''
    moves the car wheels on both sides, negative values to turn car back
    '''
    def moveCar(self, leftSpeed=0, rightSpeed=0):
        try:
            self.__eBrake.cancel()
            self.__eDist.cancel()
        except:
            pass

        if (leftSpeed > 0 and self.distance_FR > self.dist_err) or leftSpeed <= 0:
            self.leftWheel.move(leftSpeed)
            self.leftSpeed = leftSpeed

        if (rightSpeed > 0 and self.distance_FL > self.dist_err) or rightSpeed <= 0:
            self.rightWheel.move(rightSpeed)
            self.rightSpeed = rightSpeed

        self.__eDist = Timer(self.__distanceInterval,self.__observeDistance)
        self.__eDist.start()

        #setup timer
        self.__eBrake = Timer(self.__timeout,self.stop)
        self.__eBrake.start()

    '''
    stop car
    '''
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

    q = Queue(1)
    car = Car(q)
    car.start()